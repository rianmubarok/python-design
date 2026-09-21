"""
anim_ellipse_orbital.py
-----------------------
Animated abstract pattern: dual axis ellipse orbital dance.

Visual character:
- Two ellipse ring systems with different axis ratios
- One ellipse slowly rotates CW, the other CCW
- Interference between the two creates morphing lens/mandorla shapes
- Pure black-and-white seamless loop

Format: MP4 H.264, 30fps, 10s, vertical 9:16 (2160×3840)
"""

import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from video_renderer import VideoConfig, make_coords, gray_to_rgb, render_video


def ellipse_dist(X, Y, a, b, rotation):
    """Distance field stretched as ellipse with semi-axes a (x) and b (y), rotated."""
    cos_r, sin_r = np.cos(rotation), np.sin(rotation)
    Xr =  cos_r * X + sin_r * Y
    Yr = -sin_r * X + cos_r * Y
    return np.sqrt((Xr / a)**2 + (Yr / b)**2)


def frame_fn(frame_idx: int, t: float, cfg: VideoConfig) -> np.ndarray:
    X, Y = make_coords(cfg)
    angle = t * 2 * np.pi

    # Ellipse A: wide, rotating CW (speed=1)
    rot_a = angle * 1       # speed=1 (integer ✓)
    ea = ellipse_dist(X, Y, a=1.0, b=0.55, rotation=rot_a)

    # Ellipse B: tall, rotating CCW (speed=-1), different aspect
    rot_b = -angle * 1      # speed=-1 (integer ✓)
    eb = ellipse_dist(X, Y, a=0.6, b=1.0, rotation=rot_b)

    freq = 52.0
    # Rings expanding from each ellipse system
    wave_a = np.cos(ea * freq - angle * 2)   # speed=2 (integer ✓)
    wave_b = np.cos(eb * freq - angle * 2)

    combined = 0.5 * wave_a + 0.5 * wave_b

    sharpness = 18.0
    bw = np.tanh(sharpness * combined) * 0.5 + 0.5
    return gray_to_rgb(bw)


if __name__ == "__main__":
    cfg = VideoConfig(aspect="vertical", fps=30, duration=10.0, crf=18, preset="slow")
    out_dir = Path(__file__).parent.parent / "output" / "vertical"
    out_path = out_dir / "abstract animated concentric ellipse dual axis orbital dance rotation seamless loop pattern black white vertical.mp4"
    render_video(cfg, frame_fn, out_path)
