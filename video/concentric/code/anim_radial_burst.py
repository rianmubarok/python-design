"""
anim_radial_burst.py
--------------------
Animated abstract pattern: concentric rings + radial spokes burst.

Visual character:
- Concentric rings expand outward
- Radial spoke pattern overlaid, counter-rotating
- Product of ring × spokes = burst/sunburst that rotates and pulses
- High spoke count creates fine detail texture
- Pure black-and-white seamless loop

Format: MP4 H.264, 30fps, 10s, vertical 9:16 (2160×3840)
"""

import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from video_renderer import VideoConfig, make_coords, gray_to_rgb, render_video


def frame_fn(frame_idx: int, t: float, cfg: VideoConfig) -> np.ndarray:
    X, Y = make_coords(cfg)
    r     = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)
    angle = t * 2 * np.pi

    # Concentric rings — expanding outward
    ring_freq = 58.0
    rings = np.cos(r * ring_freq - angle * 2)   # speed=2 (integer ✓)

    # Radial spokes — rotating
    n_spokes = 36
    spokes = np.cos(theta * n_spokes - angle * 1)  # speed=1 (integer ✓)

    # Combine: product creates sunburst; add rings solo for background
    burst   = rings * spokes           # sunburst cells
    bg_ring = np.cos(r * 30.0 + angle * 1)  # speed=-1 slow inward  (integer ✓)

    combined = 0.5 * burst + 0.3 * rings + 0.2 * bg_ring

    sharpness = 16.0
    bw = np.tanh(sharpness * combined) * 0.5 + 0.5
    return gray_to_rgb(bw)


if __name__ == "__main__":
    cfg = VideoConfig(aspect="vertical", fps=30, duration=10.0, crf=18, preset="slow")
    out_dir = Path(__file__).parent.parent / "output" / "vertical"
    out_path = out_dir / "abstract animated concentric radial burst spokes rings rotation pulse seamless loop pattern black white vertical.mp4"
    render_video(cfg, frame_fn, out_path)
