"""
anim_hexagon_rings.py
---------------------
Animated abstract pattern: concentric hexagon rings pulsing with rotation.

Visual character:
- Rings based on TRUE hexagonal distance metric (3-axis norm)
- Creates sharp-edged hexagonal concentric pattern
- Two layers at different speeds — one expanding, one contracting
- Hex grid slowly rotates by 60° per loop (one full hex-symmetry step)
- Pure black-and-white seamless loop

Format: MP4 H.264, 30fps, 10s, vertical 9:16 (2160×3840)

Seamless loop guarantee
-----------------------
t = i / total  →  t ∈ [0, 1)  (never reaches 1)
All time-varying terms must complete an integer number of full cycles:
    cos(... - angle * N)   with N ∈ ℤ
    where angle = t * 2π  →  angle(t=1) = 2π → cos wraps exactly.

WHY THE ORIGINAL CODE BROKE:
  The original used a 4-axis hex approximation (|x|, |y|, |0.5x+…|, |0.5x-…|).
  The |y| term does NOT have 6-fold rotational symmetry, so rotating the grid
  by 60° changes individual pixel h values → cos(h*freq) doesn't wrap → jump.

THE CORRECT FIX:
  Use the TRUE 3-axis hexagonal norm:
      h = max(|u1|, |u2|, |u3|)
  where u1, u2, u3 are projections onto the three hex axes (0°, 60°, 120°).

  Proof that h is preserved under 60° rotation:
    Rotating by 60° maps (u1, u2, u3) → (u2, u3, u1)  [cyclic permutation]
    Therefore max(|u1'|, |u2'|, |u3'|) = max(|u2|, |u3|, |u1|) = h  ✓

  So h(rotate(X,Y,60°)) = h(X,Y) for EVERY pixel.
  The original grid-rotation approach is correct with this metric.
  Visual style is preserved: pure hexagonal rings with slow real grid rotation.
"""

import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from video_renderer import VideoConfig, make_coords, gray_to_rgb, render_video


def hex_dist(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """
    TRUE hexagonal distance metric — 3-axis hex norm.

    Projects onto the three hexagonal axes (0°, 60°, 120°) and takes max.
    This metric has PERFECT 6-fold rotational symmetry:
        hex_dist(rotate(X, Y, 60°)) == hex_dist(X, Y)  for all (X, Y)

    This is the key property that makes grid rotation seamlessly loopable.
    """
    sqrt3_2 = np.sqrt(3) / 2
    u1 = np.abs(X)                             # axis at   0°
    u2 = np.abs(0.5 * X + sqrt3_2 * Y)        # axis at  60°
    u3 = np.abs(-0.5 * X + sqrt3_2 * Y)       # axis at 120°
    return np.maximum(np.maximum(u1, u2), u3)


def frame_fn(frame_idx: int, t: float, cfg: VideoConfig) -> np.ndarray:
    """
    Seamless-loop frame function.

    Grid rotates 60° per loop. Because hex_dist has perfect 60° symmetry,
    h values per pixel are IDENTICAL at t=0 and t→1 → seamless loop.

    Wave speeds (must be integers):
        wave1: speed = +1  (expands outward)
        wave2: speed = -2  (contracts inward, faster)
    """
    X, Y = make_coords(cfg)
    angle = t * 2 * np.pi   # 0 → 2π over one loop

    # Rotate the hex grid by 60° over one full loop
    # hex_dist is invariant under this rotation → loop is seamless ✓
    hex_rotation = angle / 6   # 2π/6 = 60° at t→1
    cos_r = np.cos(hex_rotation)
    sin_r = np.sin(hex_rotation)
    Xr =  cos_r * X + sin_r * Y
    Yr = -sin_r * X + cos_r * Y

    h = hex_dist(Xr, Yr)   # h(t=0) == h(t→1) because 60°-rotation preserves h ✓

    freq = 55.0
    # Layer 1: expanding outward, speed = 1 (integer ✓)
    wave1 = np.cos(h * freq - angle * 1)
    # Layer 2: contracting inward, speed = -2 (integer ✓)
    wave2 = np.cos(h * freq + angle * 2)

    combined = 0.7 * wave1 + 0.3 * wave2

    sharpness = 20.0
    bw = np.tanh(sharpness * combined) * 0.5 + 0.5
    return gray_to_rgb(bw)


if __name__ == "__main__":
    cfg = VideoConfig(aspect="vertical", fps=30, duration=10.0, crf=18, preset="slow")
    out_dir = Path(__file__).parent.parent / "output" / "vertical"
    out_path = out_dir / "abstract animated concentric hexagon rings pulsing rotation seamless loop pattern black white vertical.mp4"
    render_video(cfg, frame_fn, out_path)
