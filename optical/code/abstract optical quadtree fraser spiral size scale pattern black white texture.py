import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def draw_fraser_quad(ax, x, y, size):
    """Draw a Fraser spiral twisted cord unit inside box (x, y, size)."""
    cx = x + size / 2
    cy = y + size / 2

    # Draw border frame
    rect = Rectangle(
        (x, y),
        size,
        size,
        fill=False,
        edgecolor="black",
        linewidth=1.2,
    )
    ax.add_patch(rect)

    # Concentric Fraser twisted cord rings inside the box
    num_rings = max(2, int(size / 6))
    radii = np.linspace(size * 0.15, size * 0.42, num_rings)
    tilt = np.radians(24)

    for idx, r in enumerate(radii):
        n_elem = int(12 + idx * 6)
        angles = np.linspace(0, 2 * np.pi, n_elem, endpoint=False)
        seg_len = size * 0.12

        for a in angles:
            px = cx + r * np.cos(a)
            py = cy + r * np.sin(a)
            dir_a = a + np.pi / 2 + tilt

            dx = (seg_len / 2) * np.cos(dir_a)
            dy = (seg_len / 2) * np.sin(dir_a)

            ax.plot(
                [px - dx, px + dx],
                [py - dy, py + dy],
                color="black",
                linewidth=1.8,
            )


def subdivide(ax, x, y, size, depth):
    if depth > 0 and (depth >= 3 or np.random.rand() < 0.68):
        half = size / 2.0
        subdivide(ax, x, y, half, depth - 1)
        subdivide(ax, x + half, y, half, depth - 1)
        subdivide(ax, x, y + half, half, depth - 1)
        subdivide(ax, x + half, y + half, half, depth - 1)
    else:
        draw_fraser_quad(ax, x, y, size)


def abstract_optical_quadtree_fraser_spiral_size_scale_pattern_black_white_texture():
    """Optical experiment: Quadtree recursive subdivision filled with Fraser spiral twisted cord units."""
    fig, ax = setup_ax()

    subdivide(ax, -46, -46, 92, depth=3)

    save(
        fig,
        "abstract optical quadtree fraser spiral size scale pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_quadtree_fraser_spiral_size_scale_pattern_black_white_texture()
