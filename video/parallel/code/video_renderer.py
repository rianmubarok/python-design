"""
video_renderer.py
-----------------
Base rendering pipeline for animated abstract pattern videos.

Usage:
    from video_renderer import VideoConfig, render_video

    config = VideoConfig(aspect="vertical")

    def my_frame_fn(frame_idx: int, t: float, cfg: VideoConfig) -> np.ndarray:
        # Return HxWx3 uint8 numpy array (RGB)
        ...

    render_video(config, my_frame_fn, output_path="output/vertical/my_pattern.mp4")
"""

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ASPECT_PRESETS = {
    "vertical":  {"width": 2160, "height": 3840},  # 9:16
    "landscape": {"width": 3840, "height": 2160},  # 16:9
    "square":    {"width": 2160, "height": 2160},  # 1:1
}


@dataclass
class VideoConfig:
    """
    Holds all parameters for a single video render.

    Parameters
    ----------
    aspect : str
        One of "vertical", "landscape", "square".
    fps : int
        Frames per second (default 30).
    duration : float
        Duration in seconds (default 10.0).
    crf : int
        H.264 CRF quality (0=lossless, 23=default, 18=near-lossless).
        Lower = larger file / better quality. 18 is good for stock.
    preset : str
        ffmpeg encoding preset. "slow" gives better compression quality.
    """
    aspect: str = "vertical"
    fps: int = 30
    duration: float = 10.0
    crf: int = 18
    preset: str = "slow"
    extra: dict = field(default_factory=dict)  # hook for per-animation params

    @property
    def width(self) -> int:
        return ASPECT_PRESETS[self.aspect]["width"]

    @property
    def height(self) -> int:
        return ASPECT_PRESETS[self.aspect]["height"]

    @property
    def total_frames(self) -> int:
        return int(self.fps * self.duration)


# ---------------------------------------------------------------------------
# FrameFunction type alias
# ---------------------------------------------------------------------------

# Callable(frame_index, normalized_time [0..1), config) -> np.ndarray HxWx3 uint8
FrameFunction = Callable[[int, float, VideoConfig], np.ndarray]


# ---------------------------------------------------------------------------
# Core renderer
# ---------------------------------------------------------------------------

def render_video(
    config: VideoConfig,
    frame_fn: FrameFunction,
    output_path: str | Path,
    verbose: bool = True,
) -> Path:
    """
    Render an animation to an MP4 file by piping raw RGB frames to ffmpeg.

    Parameters
    ----------
    config : VideoConfig
        Resolution, fps, duration and encoding settings.
    frame_fn : FrameFunction
        Called for each frame. Must return HxWx3 uint8 RGB numpy array.
    output_path : str or Path
        Destination MP4 file path.
    verbose : bool
        Print progress to stdout.

    Returns
    -------
    Path
        Resolved path to the output file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    W, H = config.width, config.height
    total = config.total_frames

    # Build ffmpeg command -------------------------------------------------
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(config.fps),
        "-i", "pipe:0",           # read raw RGB from stdin
        "-vcodec", "libx264",
        "-pix_fmt", "yuv420p",    # required for broad player compatibility
        "-crf", str(config.crf),
        "-preset", config.preset,
        "-an",                    # no audio
        str(output_path),
    ]

    if verbose:
        print(f"[render] {output_path.name}  {W}×{H}  {config.fps}fps  "
              f"{total} frames  ({config.duration:.0f}s)")

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )

    try:
        for i in range(total):
            t = i / total  # normalised time in [0, 1)
            frame = frame_fn(i, t, config)

            # Validate frame shape
            if frame.shape != (H, W, 3):
                raise ValueError(
                    f"frame_fn returned shape {frame.shape}, expected ({H}, {W}, 3)"
                )

            proc.stdin.write(frame.astype(np.uint8).tobytes())

            if verbose and (i % config.fps == 0 or i == total - 1):
                pct = (i + 1) / total * 100
                print(f"\r  {i+1:5d}/{total}  {pct:5.1f}%", end="", flush=True)

        proc.stdin.close()

    except Exception as exc:
        proc.kill()
        _, stderr = proc.communicate()
        print(f"\n[ERROR] ffmpeg stderr:\n{stderr.decode()}", file=sys.stderr)
        raise exc

    _, stderr = proc.communicate()
    if proc.returncode != 0:
        print(f"\n[ERROR] ffmpeg failed:\n{stderr.decode()}", file=sys.stderr)
        raise RuntimeError(f"ffmpeg exited with code {proc.returncode}")

    if verbose:
        size_mb = output_path.stat().st_size / 1_048_576
        print(f"\n  done → {output_path}  ({size_mb:.1f} MB)")

    return output_path


# ---------------------------------------------------------------------------
# Helpers for frame functions
# ---------------------------------------------------------------------------

def make_coords(config: VideoConfig) -> tuple[np.ndarray, np.ndarray]:
    """
    Return (X, Y) coordinate grids normalised to [-1, 1] on the shorter axis.

    For vertical (2160×3840):
        X ∈ [-1, 1]   (width axis)
        Y ∈ [-1.778, 1.778] approximate  (height axis, scaled equally)

    This makes it easy to write aspect-ratio-aware formulas.
    """
    W, H = config.width, config.height
    scale = 2.0 / min(W, H)
    xs = (np.arange(W) - W / 2) * scale
    ys = (np.arange(H) - H / 2) * scale
    X, Y = np.meshgrid(xs, ys)
    return X, Y


def gray_to_rgb(arr: np.ndarray) -> np.ndarray:
    """Convert HxW float array [0..1] → HxWx3 uint8 RGB (greyscale)."""
    c = (np.clip(arr, 0.0, 1.0) * 255).astype(np.uint8)
    return np.stack([c, c, c], axis=-1)


def bw_to_rgb(arr: np.ndarray, invert: bool = False) -> np.ndarray:
    """Convert HxW float field → black-and-white HxWx3 uint8 by thresholding at 0.5."""
    if invert:
        arr = 1.0 - arr
    binary = (arr > 0.5).astype(np.uint8) * 255
    return np.stack([binary, binary, binary], axis=-1)


def smooth_loop(t: float, fn: Callable[[float], float]) -> float:
    """
    Wrap a [0,1) time value so that fn(0) == fn(1) for seamless looping.
    Uses a full 2π cycle: angle = t * 2π.
    """
    return fn(t * 2 * np.pi)
