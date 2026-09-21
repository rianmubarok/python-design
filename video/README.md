# RUPA Animated Pattern — Video Pipeline

Animated abstract patterns untuk stock video (Shutterstock, Adobe Stock).
Pure Python + NumPy + ffmpeg. No OpenCV required.

---

## Stack

| Tool | Role |
|------|------|
| Python 3.12 | Frame generation |
| NumPy | Vectorised pixel math |
| ffmpeg (system) | H.264 encoding via stdin pipe |

---

## Output Format

| Spec | Value |
|------|-------|
| Container | MP4 |
| Codec | H.264 (libx264) |
| Pixel format | yuv420p |
| FPS | 30 |
| Duration | 10 seconds |
| Audio | None |
| CRF | 18 (near-lossless for stock) |

---

## Aspect Ratios

| Name | Resolution | Aspect |
|------|-----------|--------|
| vertical | 2160 × 3840 | 9:16 |
| landscape | 3840 × 2160 | 16:9 |
| square | 2160 × 2160 | 1:1 |

**Priority order:** vertical → landscape → square → cinematic

---

## Structure

```
video/
├── code/
│   ├── video_renderer.py          ← base pipeline (import this)
│   ├── anim_concentric_waves.py   ← expanding concentric rings
│   ├── anim_flowing_lines.py      ← flowing parallel sine-wave lines
│   └── anim_geometric_rotation.py ← counter-rotating polar moiré
└── output/
    ├── vertical/                  ← 2160×3840 renders
    ├── landscape/                 ← 3840×2160 renders
    └── square/                    ← 2160×2160 renders
```

---

## How to Run

```bash
# Single animation (vertical 4K, ~3–5 min on a modern CPU)
python video/code/anim_concentric_waves.py

# All three animations sequentially
python video/code/anim_concentric_waves.py
python video/code/anim_flowing_lines.py
python video/code/anim_geometric_rotation.py
```

Output MP4s land in `video/output/vertical/`.

---

## How to Add a New Animation

1. Create `video/code/anim_<name>.py`
2. Import `VideoConfig`, `make_coords`, `gray_to_rgb`, `render_video` from `video_renderer`
3. Write a `frame_fn(frame_idx, t, cfg) -> np.ndarray` that returns `H×W×3 uint8`
   - `t` is normalised time `[0, 1)` — design so `t=0` and `t=1` match for seamless loop
   - Use `angle = t * 2 * np.pi` as loop phase
4. Call `render_video(cfg, frame_fn, output_path)`

```python
def frame_fn(frame_idx, t, cfg):
    X, Y = make_coords(cfg)
    angle = t * 2 * np.pi
    # ... your math here ...
    return gray_to_rgb(bw_field)
```

---

## Seamless Loop Design Rule

All animations use `angle = t * 2 * np.pi` as the primary phase variable.
Because `cos(x + 2π) == cos(x)`, when `t` wraps from `1.0` back to `0.0`
the first and last frame are identical → perfect seamless loop.

---

## Animations

### 1. Concentric Waves — `anim_concentric_waves.py`
Three concentric ring systems at different spatial frequencies expanding outward.
Interference between layers creates rich depth. Rings pulse outward continuously.

### 2. Flowing Lines — `anim_flowing_lines.py`
Horizontal line field displaced by a sum of travelling sine waves.
Two waves run in opposite directions, one adds diagonal drift.
Gives a flowing fabric / water-surface feel.

### 3. Geometric Rotation — `anim_geometric_rotation.py`
Radial spoke pattern (CW) × concentric rings (CCW) + spiral twist.
Counter-rotation creates moiré interference fringes and a hypnotic optical illusion.
