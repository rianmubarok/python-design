"""
anim_dual_source_ripple.py
--------------------------
Animated abstract pattern: dual source ripple interference.

Visual character:
- Two ring centers slowly orbit each other in a circle
- Rings from both sources interfere → shifting moire/interference pattern
- Centers complete one full orbit per loop → seamless
- Pure black-and-white, suitable as vertical abstract background

Format: MP4 H.264, 30fps, 10s, vertical 9:16 (2160×3840)
"""

import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from video_renderer import VideoConfig, make_coords, gray_to_rgb, render_video


def frame_fn(frame_idx: int, t: float, cfg: VideoConfig) -> np.ndarray:
    X, Y = make_coords(cfg)
    angle = t * 2 * np.pi   # seamless loop phase

    # Two centers orbit around origin — one full revolution per loop
    # orbit_r in normalised coords (X ∈ [-1,1] on short axis)
    orbit_r = 0.45
    cx1 =  orbit_r * np.cos(angle * 1)   # speed = 1 (integer ✓)
    cy1 =  orbit_r * np.sin(angle * 1)
    cx2 = -orbit_r * np.cos(angle * 1)   # opposite side
    cy2 = -orbit_r * np.sin(angle * 1)

    # Distance from each center
    r1 = np.sqrt((X - cx1)**2 + (Y - cy1)**2)
    r2 = np.sqrt((X - cx2)**2 + (Y - cy2)**2)

    # Rings from each source — expanding outward, same speed
    freq = 50.0
    wave1 = np.cos(r1 * freq - angle * 2)   # speed = 2 (integer ✓)
    wave2 = np.cos(r2 * freq - angle * 2)

    # Interference: sum then normalize
    combined = (wave1 + wave2) * 0.5

    sharpness = 18.0
    bw = np.tanh(sharpness * combined) * 0.5 + 0.5
    return gray_to_rgb(bw)


if __name__ == "__main__":
    cfg = VideoConfig(aspect="vertical", fps=30, duration=10.0, crf=18, preset="slow")
    out_dir = Path(__file__).parent.parent / "output" / "vertical"
    out_path = out_dir / "abstract animated concentric dual source ripple interference orbit seamless loop pattern black white vertical.mp4"
    render_video(cfg, frame_fn, out_path)
