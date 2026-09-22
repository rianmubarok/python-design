import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("black")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="black")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="black")
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def draw_petal(ax, cx, cy, r_inner, r_outer, angle, petal_w_frac=0.38, fill="white"):
    """Draw one mandala petal: a pointed lens shape radiating outward at `angle`."""
    half_arc = np.pi * petal_w_frac
    # Outer arc
    theta_out = np.linspace(angle - half_arc / 2, angle + half_arc / 2, 40)
    ox = cx + r_outer * np.cos(theta_out)
    oy = cy + r_outer * np.sin(theta_out)
    # Inner arc (reversed)
    theta_in = np.linspace(angle + half_arc / 2, angle - half_arc / 2, 40)
    ix = cx + r_inner * np.cos(theta_in)
    iy = cy + r_inner * np.sin(theta_in)
    pts = np.column_stack([np.concatenate([ox, ix]),
                           np.concatenate([oy, iy])])
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor="none", zorder=2))


def draw_eye_iris_mandala(ax, cx, cy, R, n_petals, rotation=0.0, fill="white"):
    """Layered mandala built from:
      - Outer ring of `n_petals` leaf petals
      - Mid ring of shorter petals (rotated by half step)
      - Iris concentric circles
      - Pupil (dark circle)
      - Highlight dot
    Combines halloween eyeball iris + mandala petal geometry."""
    inv = "black" if fill == "white" else "white"

    # === OUTER PETAL RING ===
    angles = np.linspace(0, 2 * np.pi, n_petals, endpoint=False) + rotation
    for ang in angles:
        draw_petal(ax, cx, cy, R * 0.52, R * 1.00, ang,
                   petal_w_frac=0.55, fill=fill)

    # === MID PETAL RING (half-step rotation, shorter) ===
    angles_mid = angles + np.pi / n_petals
    for ang in angles_mid:
        draw_petal(ax, cx, cy, R * 0.40, R * 0.70, ang,
                   petal_w_frac=0.45, fill=inv)

    # === IRIS RINGS ===
    # Outermost iris (white sclera disc)
    ax.add_patch(Circle((cx, cy), R * 0.50,
                        facecolor=fill, edgecolor="none", zorder=3))
    # Iris colour ring
    ax.add_patch(Circle((cx, cy), R * 0.38,
                        facecolor=inv, edgecolor="none", zorder=4))
    # Iris radial lines (spokes)
    n_iris = n_petals * 2
    for k in range(n_iris):
        a = k * 2 * np.pi / n_iris + rotation
        x0 = cx + R * 0.20 * np.cos(a); y0 = cy + R * 0.20 * np.sin(a)
        x1 = cx + R * 0.36 * np.cos(a); y1 = cy + R * 0.36 * np.sin(a)
        ax.plot([x0, x1], [y0, y1], color=fill, lw=0.6, zorder=5)

    # Pupil
    ax.add_patch(Circle((cx, cy), R * 0.18,
                        facecolor=fill, edgecolor="none", zorder=6))
    # Inner pupil (deep dark)
    ax.add_patch(Circle((cx, cy), R * 0.12,
                        facecolor=inv, edgecolor="none", zorder=7))
    # Highlight
    ax.add_patch(Circle((cx + R * 0.06, cy + R * 0.05), R * 0.04,
                        facecolor=fill, edgecolor="none", zorder=8))


def draw():
    """3×3 grid of eye-iris mandala tiles.
    Alternating tiles swap fill/background. Rotation offset per tile.
    Seamless via WRAPS."""
    fig, ax = setup_ax()

    cols, rows = 3, 3
    dx, dy = PERIOD / cols, PERIOD / rows
    R = min(dx, dy) * 0.46

    rotations = np.radians([0, 20, 10, 30, 5, 25, 15, 35, 8])
    n_petals_seq = [8, 10, 8, 10, 8, 10, 8, 10, 8]

    idx = 0
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            fill = "white" if (row + col) % 2 == 0 else "#cccccc"
            rot  = rotations[idx % len(rotations)]
            np_  = n_petals_seq[idx % len(n_petals_seq)]
            idx += 1

            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    draw_eye_iris_mandala(ax, px, py, R, np_, rotation=rot, fill=fill)

    save(fig, "abstract halloween variation eye iris radial petal mandala combo pattern black white texture")


if __name__ == "__main__":
    draw()
