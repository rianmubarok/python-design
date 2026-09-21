"""
anim_geometric_rotation.py
--------------------------
Animated abstract pattern: rotating geometric optical illusion.

Visual character:
- Pure black-and-white
- Polar grid of radial lines and rings rotating in opposite directions
- Creates optical illusion / hypnotic spin effect
- Two counter-rotating layers produce moiré-style interference fringes
- Seamless loop (full 360° rotation over 10 seconds)

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
    Two overlapping polar stripe patterns rotating in opposite directions.

    Layer A: radial stripes (angular stripes) rotating CW
    Layer B: concentric rings rotating CCW at different speed
    Combined via multiplication → interference moiré pattern
    """
    X, Y = make_coords(cfg)

    r     = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)   # [-π, π]

    angle = t * 2 * np.pi   # seamless loop angle

    # Seamless loop rule: all speed multipliers MUST be integers.
    # cos(x + speed * 2π) = cos(x) when speed is integer → frame 0 = frame N.

    # --- Layer A: angular / radial stripes, 1 full CW rotation per loop ---
    n_spokes = 24
    rot_a    = angle * 1    # speed = 1 (integer ✓)
    wave_a   = np.cos(theta * n_spokes - rot_a)

    # --- Layer B: concentric rings, 1 CCW rotation per loop ---
    ring_freq = 9.0
    rot_b     = -angle * 1  # speed = -1, CCW (integer ✓)
    wave_b    = np.cos(r * ring_freq - rot_b)

    # --- Combine: product creates moiré / interference ---
    combined = wave_a * wave_b

    # Soft vignette so edges don't look harsh at crop
    vignette = np.clip(1.0 - (r / 2.2) ** 3, 0.0, 1.0)

    # Spiral twist with integer speed
    twist_strength = 0.8
    twist = np.cos(theta * n_spokes + r * ring_freq * twist_strength - angle * 2)  # speed = 2 (integer ✓)
    combined = 0.7 * combined + 0.3 * twist

    # Apply vignette to keep centre active
    field = combined * vignette

    # Sharpen
    sharpness = 7.0
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
    out_path = out_dir / "abstract animated geometric rotation optical illusion moiré seamless loop pattern black white vertical.mp4"

    render_video(cfg, frame_fn, out_path)
