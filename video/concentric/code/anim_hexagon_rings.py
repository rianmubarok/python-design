"""
anim_hexagon_rings.py
---------------------
Animated abstract pattern: concentric hexagon rings pulsing.

Visual character:
- Rings based on hexagonal distance metric instead of circular
- Creates sharp-edged hexagonal concentric pattern
- Two layers at different speeds — one expanding, one contracting
- Pure black-and-white seamless loop

Format: MP4 H.264, 30fps, 10s, vertical 9:16 (2160×3840)
"""

import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from video_renderer import VideoConfig, make_coords, gray_to_rgb, render_video


def hex_dist(X, Y, rotation=0.0):
    """Hexagonal distance metric (Chebyshev on rotated hex grid)."""
    # Rotate
    cos_r, sin_r = np.cos(rotation), np.sin(rotation)
    Xr =  cos_r * X + sin_r * Y
    Yr = -sin_r * X + cos_r * Y
    # Hex metric: max(|x|, |y|, |x+y|/√3... use axial approx)
    # Simple hex approximation: combine abs values on 3 axes
    a1 = np.abs(Xr)
    a2 = np.abs(Yr)
    a3 = np.abs(Xr * 0.5 + Yr * np.sqrt(3) / 2)
    a4 = np.abs(Xr * 0.5 - Yr * np.sqrt(3) / 2)
    return np.maximum(np.maximum(a1, a2), np.maximum(a3, a4))


def frame_fn(frame_idx: int, t: float, cfg: VideoConfig) -> np.ndarray:
    X, Y = make_coords(cfg)
    angle = t * 2 * np.pi

    # Slowly rotate the hex grid itself — speed = 1 (integer ✓)
    hex_rotation = angle * 1 / 6   # 1/6 turn per loop = 60° = one hex symmetry step

    h = hex_dist(X, Y, rotation=hex_rotation)

    freq = 55.0
    # Layer 1: expanding outward, speed=1
    wave1 = np.cos(h * freq - angle * 1)    # speed=1 (integer ✓)
    # Layer 2: contracting inward, speed=-2 (faster)
    wave2 = np.cos(h * freq + angle * 2)    # speed=-2 (integer ✓)

    combined = 0.7 * wave1 + 0.3 * wave2

    sharpness = 20.0
    bw = np.tanh(sharpness * combined) * 0.5 + 0.5
    return gray_to_rgb(bw)


if __name__ == "__main__":
    cfg = VideoConfig(aspect="vertical", fps=30, duration=10.0, crf=18, preset="slow")
    out_dir = Path(__file__).parent.parent / "output" / "vertical"
    out_path = out_dir / "abstract animated concentric hexagon rings pulsing rotation seamless loop pattern black white vertical.mp4"
    render_video(cfg, frame_fn, out_path)
