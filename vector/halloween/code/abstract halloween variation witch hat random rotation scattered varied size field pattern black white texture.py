import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Polygon, FancyBboxPatch
from matplotlib.path import Path as MPath
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
    ax.set_facecolor("white")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def draw_witch_hat(ax, cx, cy, s, angle=0.0, fill="black"):
    """Witch hat: tall cone + wide brim, rotated by angle."""
    edge = "none" if fill == "black" else "black"
    elw = 0.0 if fill == "black" else 0.8

    def rot(x, y):
        rx = (x - cx) * np.cos(angle) - (y - cy) * np.sin(angle) + cx
        ry = (x - cx) * np.sin(angle) + (y - cy) * np.cos(angle) + cy
        return rx, ry

    # Cone (tall triangle)
    tip_x, tip_y = cx, cy + s * 0.52
    bl_x, bl_y = cx - s * 0.18, cy - s * 0.08
    br_x, br_y = cx + s * 0.18, cy - s * 0.08
    cone = [[tip_x, tip_y], [bl_x, bl_y], [br_x, br_y]]
    cx_r, cy_r = rot(np.array([p[0] for p in cone]), np.array([p[1] for p in cone]))
    ax.add_patch(Polygon(np.column_stack([cx_r, cy_r]),
                         closed=True, facecolor=fill, edgecolor=edge, linewidth=elw))

    # Brim (wide ellipse)
    t = np.linspace(0, 2 * np.pi, 60)
    bx = cx + s * 0.32 * np.cos(t)
    by = cy - s * 0.07 + s * 0.085 * np.sin(t)
    rx, ry = rot(bx, by)
    ax.add_patch(Polygon(np.column_stack([rx, ry]),
                         closed=True, facecolor=fill, edgecolor=edge, linewidth=elw))

    # Hat band stripe
    band_pts_x = np.array([bl_x, br_x, br_x + 0.01 * s, bl_x - 0.01 * s])
    band_pts_y = np.array([cy - s * 0.05, cy - s * 0.05,
                           cy + s * 0.03, cy + s * 0.03])
    band_c = "white" if fill == "black" else "black"
    rbx, rby = rot(band_pts_x, band_pts_y)
    ax.add_patch(Polygon(np.column_stack([rbx, rby]),
                         closed=True, facecolor=band_c, edgecolor="none"))


def draw():
    """Scattered field of witch hats with random sizes and rotations.
    Uses a fixed RNG seed for reproducible tiling (positions tile seamlessly
    via WRAPS). Hats range from tiny to large on white background."""
    fig, ax = setup_ax()

    rng = np.random.default_rng(7)
    n_hats = 30

    # Generate positions and params in [0, PERIOD) so tiling works
    positions = rng.uniform(0, PERIOD, (n_hats, 2))
    angles = rng.uniform(-np.pi, np.pi, n_hats)
    sizes = rng.uniform(3.5, 10.0, n_hats)

    for i in range(n_hats):
        cx, cy = positions[i]
        for ox, oy in WRAPS:
            px, py = cx + ox, cy + oy
            if -12 <= px <= PERIOD + 12 and -12 <= py <= PERIOD + 12:
                draw_witch_hat(ax, px, py, sizes[i], angle=angles[i], fill="black")

    save(fig, "abstract halloween variation witch hat random rotation scattered varied size field pattern black white texture")


if __name__ == "__main__":
    draw()
