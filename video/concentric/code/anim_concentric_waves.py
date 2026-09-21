"""
anim_concentric_waves.py
------------------------
Animated abstract pattern: concentric expanding rings.

Visual character:
- Pure black-and-white
- Concentric rings pulse outward in a seamless loop
- Multiple ring systems at different phases create depth
- Subtle radius modulation adds organic feel
- Suitable as vertical abstract background

Format: MP4 H.264, 30fps, 10s, vertical 9:16 (2160×3840)
"""

import sys
from pathlib import Path

import numpy as np

# Allow import from sibling location when run directly
sys.path.insert(0, str(Path(__file__).parent))
from video_renderer import VideoConfig, make_coords, gray_to_rgb, render_video


# ---------------------------------------------------------------------------
# Frame function
# ---------------------------------------------------------------------------

def frame_fn(frame_idx: int, t: float, cfg: VideoConfig) -> np.ndarray:
    """
    t ∈ [0, 1)  — normalised loop time

    Seamless loop rule: all speed values MUST be integers (or zero).
    Phase at t=1.0 = speed * 2π = integer * 2π → cos returns to exact start value.

    Ring formula:
        value = cos(r * freq - t * speed * 2π)
    """
    X, Y = make_coords(cfg)
    r = np.sqrt(X**2 + Y**2)

    angle = t * 2 * np.pi   # one full cycle per loop

    # Primary ring system — rings expand outward, 1 full cycle per loop
    # freq=60 → ~10 rings visible in half-frame at 2160px width
    freq1  = 60.0
    wave1  = np.cos(r * freq1 - angle * 1)   # speed = 1 (integer ✓)

    # Secondary ring system — slightly denser, faster expansion
    freq2  = 40.0
    wave2  = np.cos(r * freq2 - angle * 2)   # speed = 2 (integer ✓)

    # Tertiary — slower rings drifting inward for depth/interference
    freq3  = 25.0
    wave3  = np.cos(r * freq3 + angle * 1)   # speed = -1 → inward (integer ✓)

    # Combine with weights
    combined = 0.55 * wave1 + 0.30 * wave2 + 0.15 * wave3

    # Sharpen into crisp black-and-white rings via tanh thresholding
    # sharpness=20 gives clean hard edges without aliasing
    sharpness = 20.0
    bw = np.tanh(sharpness * combined) * 0.5 + 0.5   # remap to [0, 1]

    return gray_to_rgb(bw)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    cfg = VideoConfig(
        aspect="vertical",
        fps=30,
        duration=10.0,
        crf=18,
        preset="slow",
    )

    out_dir = Path(__file__).parent.parent / "output" / "vertical"
    out_path = out_dir / "abstract animated concentric waves expanding seamless loop pattern black white vertical.mp4"

    render_video(cfg, frame_fn, out_path)
