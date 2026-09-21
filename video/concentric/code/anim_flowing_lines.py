"""
anim_flowing_lines.py
---------------------
Animated abstract pattern: flowing parallel sine-wave lines.

Visual character:
- Pure black-and-white horizontal lines
- Lines undulate with a travelling sine wave — creates flowing / fabric feel
- Wave amplitude and frequency vary subtly over time for organic movement
- Multiple overlapping wave layers with different speeds
- Seamless loop

Format: MP4 H.264, 30fps, 10s, vertical 9:16 (2160×3840)
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from video_renderer import VideoConfig, make_coords, gray_to_rgb, render_video


# ---------------------------------------------------------------------------
# Frame function
# ---------------------------------------------------------------------------

def frame_fn(frame_idx: int, t: float, cfg: VideoConfig) -> np.ndarray:
    """
    Horizontal lines deformed by vertically-travelling sine waves.

    Line field:  value = cos(Y * line_freq + displacement(X, t))
    displacement is a sum of sine waves that travel along X over time.
    """
    X, Y = make_coords(cfg)

    angle = t * 2 * np.pi   # full cycle → seamless loop

    # Seamless loop rule: all speed values MUST be integers.
    # sin(x + speed * 2π) = sin(x) when speed is integer → frame 0 = frame N.

    # --- Wave layer 1: broad gentle swell, 1 cycle per loop ---
    amp1    = 0.35
    freq_x1 = 3.0
    disp1   = amp1 * np.sin(X * freq_x1 + angle * 1)   # speed = 1 (integer ✓)

    # --- Wave layer 2: tighter ripple in opposite direction, 2 cycles per loop ---
    amp2    = 0.18
    freq_x2 = 7.0
    disp2   = amp2 * np.sin(X * freq_x2 - angle * 2)   # speed = -2 (integer ✓)

    # --- Wave layer 3: slow diagonal drift, 1 cycle per loop ---
    amp3    = 0.10
    freq_x3 = 1.5
    disp3   = amp3 * np.sin(X * freq_x3 + Y * 0.5 + angle * 1)   # speed = 1 (integer ✓)

    displacement = disp1 + disp2 + disp3

    # Line density — how many lines fill the frame vertically
    line_freq = 18.0
    field = np.cos((Y + displacement) * line_freq)

    # Sharpen to crisp B&W lines
    sharpness = 10.0
    bw = np.tanh(sharpness * field) * 0.5 + 0.5

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
    out_path = out_dir / "abstract animated flowing parallel lines wave seamless loop pattern black white vertical.mp4"

    render_video(cfg, frame_fn, out_path)
