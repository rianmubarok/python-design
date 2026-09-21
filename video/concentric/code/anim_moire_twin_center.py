"""
anim_moire_twin_center.py
-------------------------
Animated abstract pattern: moire twin center offset rings.

Visual character:
- Two concentric ring systems with fixed offset between centers
- Offset slowly drifts in a circle → shifting moire interference bands
- Creates hypnotic lens / eye pattern that morphs over time
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
    angle = t * 2 * np.pi

    # Center offset drifts in a slow circle — speed=1 (integer ✓)
    # Offset is small so rings mostly overlap → strong moire
    offset = 0.25
    ox = offset * np.cos(angle * 1)
    oy = offset * np.sin(angle * 1)

    r1 = np.sqrt((X - ox)**2 + (Y - oy)**2)
    r2 = np.sqrt((X + ox)**2 + (Y + oy)**2)

    freq = 62.0
    # Both systems expand at same speed — interference pattern morphs due to center shift
    wave1 = np.cos(r1 * freq - angle * 2)   # speed=2 (integer ✓)
    wave2 = np.cos(r2 * freq - angle * 2)

    # Interference via multiplication gives sharper moire bands
    moire = wave1 * wave2

    # Add direct sum for secondary structure
    combined = 0.6 * moire + 0.4 * (wave1 + wave2) * 0.5

    sharpness = 20.0
    bw = np.tanh(sharpness * combined) * 0.5 + 0.5
    return gray_to_rgb(bw)


if __name__ == "__main__":
    cfg = VideoConfig(aspect="vertical", fps=30, duration=10.0, crf=18, preset="slow")
    out_dir = Path(__file__).parent.parent / "output" / "vertical"
    out_path = out_dir / "abstract animated concentric moire twin center offset interference morphing seamless loop pattern black white vertical.mp4"
    render_video(cfg, frame_fn, out_path)
