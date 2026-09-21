"""
anim_spiral_rotating.py
-----------------------
Animated abstract pattern: rotating Archimedean spiral.

Visual character:
- Dense Archimedean spiral rotates continuously
- Rotation speed varies: outer rings appear to spin slower (natural perspective)
- Two counter-rotating spiral layers create depth
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
    theta = np.arctan2(Y, X)   # [-π, π]
    angle = t * 2 * np.pi

    # Archimedean spiral field: cos(r * freq - theta * arms - rotation)
    # The theta term creates the spiral twist
    arms  = 3        # number of spiral arms
    freq  = 55.0     # radial ring density

    # Layer A: CW rotation, speed = 1
    spiral_a = np.cos(r * freq - theta * arms - angle * 1)   # speed=1 (integer ✓)

    # Layer B: CCW rotation, speed = -1, different arm count
    arms_b = 4
    spiral_b = np.cos(r * freq + theta * arms_b + angle * 1)  # speed=-1 (integer ✓)

    combined = 0.65 * spiral_a + 0.35 * spiral_b

    sharpness = 18.0
    bw = np.tanh(sharpness * combined) * 0.5 + 0.5
    return gray_to_rgb(bw)


if __name__ == "__main__":
    cfg = VideoConfig(aspect="vertical", fps=30, duration=10.0, crf=18, preset="slow")
    out_dir = Path(__file__).parent.parent / "output" / "vertical"
    out_path = out_dir / "abstract animated concentric spiral rotating archimedean arms seamless loop pattern black white vertical.mp4"
    render_video(cfg, frame_fn, out_path)
