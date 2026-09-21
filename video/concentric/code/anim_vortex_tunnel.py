"""
anim_vortex_tunnel.py
---------------------
Animated abstract pattern: vortex tunnel depth illusion.

Visual character:
- Concentric rings combined with angular twist that increases with radius
- Creates a spinning tunnel / vortex depth illusion
- Inner rings appear to spin faster than outer — natural perspective feel
- Counter-rotating layers add hypnotic depth
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

    # Twist amount increases toward center (1/r) → tunnel perspective
    # Clamp r to avoid division by zero at exact center
    r_safe = np.maximum(r, 0.01)
    twist  = theta + 2.5 / r_safe   # spiral tightens toward center

    freq = 55.0

    # Layer A: vortex tunnel rotating CW, speed=1
    tunnel_a = np.cos(r * freq + twist - angle * 1)   # speed=1 (integer ✓)

    # Layer B: counter-rotating, speed=-1, different twist sign
    twist_b  = theta - 1.8 / r_safe
    tunnel_b = np.cos(r * freq + twist_b + angle * 1)  # speed=-1 (integer ✓)

    combined = 0.6 * tunnel_a + 0.4 * tunnel_b

    sharpness = 18.0
    bw = np.tanh(sharpness * combined) * 0.5 + 0.5
    return gray_to_rgb(bw)


if __name__ == "__main__":
    cfg = VideoConfig(aspect="vertical", fps=30, duration=10.0, crf=18, preset="slow")
    out_dir = Path(__file__).parent.parent / "output" / "vertical"
    out_path = out_dir / "abstract animated concentric vortex tunnel depth illusion spinning seamless loop pattern black white vertical.mp4"
    render_video(cfg, frame_fn, out_path)
