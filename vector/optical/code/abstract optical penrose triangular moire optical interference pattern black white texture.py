import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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


def draw_penrose_unit(ax, cx, cy, s):
    """Draw an impossible triangle motif at (cx, cy) of scale s."""
    # Outer triangle
    h = s * np.sqrt(3) / 2
    t1 = np.array([cx, cy + (2 / 3) * h])
    t2 = np.array([cx + s / 2, cy - (1 / 3) * h])
    t3 = np.array([cx - s / 2, cy - (1 / 3) * h])

    # Inner triangle offset
    s_in = s * 0.45
    h_in = s_in * np.sqrt(3) / 2
    i1 = np.array([cx, cy + (2 / 3) * h_in])
    i2 = np.array([cx + s_in / 2, cy - (1 / 3) * h_in])
    i3 = np.array([cx - s_in / 2, cy - (1 / 3) * h_in])

    # Draw interlocking ribbon facets
    f1 = Polygon([t1, t2, i2, i1], closed=True, facecolor="black", edgecolor="black")
    f2 = Polygon([t2, t3, i3, i2], closed=True, facecolor="white", edgecolor="black", linewidth=1.5)
    f3 = Polygon([t3, t1, i1, i3], closed=True, facecolor="black", edgecolor="black")

    ax.add_patch(f1)
    ax.add_patch(f2)
    ax.add_patch(f3)


def abstract_optical_penrose_triangular_moire_optical_interference_pattern_black_white_texture():
    """Optical experiment: Penrose impossible triangle lattice with Moiré radial wave interference overlays."""
    fig, ax = setup_ax()

    # Draw high-density background Moiré concentric interference rings
    r_vals = np.linspace(2, 65, 80)
    for r in r_vals:
        circle = plt.Circle(
            (0, 0), r, fill=False, edgecolor="black", linewidth=0.8, alpha=0.4
        )
        ax.add_patch(circle)

    # Secondary offset Moiré center creating interference wave beats
    for r in r_vals:
        circle = plt.Circle(
            (8, -6), r, fill=False, edgecolor="black", linewidth=0.6, alpha=0.3
        )
        ax.add_patch(circle)

    # Triangular grid of Penrose impossible triangles
    n_rings = 3
    for r_idx in range(1, n_rings + 1):
        radius = r_idx * 15.0
        n_units = r_idx * 6
        angles = np.linspace(0, 2 * np.pi, n_units, endpoint=False)
        for a in angles:
            cx = radius * np.cos(a)
            cy = radius * np.sin(a)
            draw_penrose_unit(ax, cx, cy, 11.0)

    # Central Penrose unit
    draw_penrose_unit(ax, 0, 0, 16.0)

    save(
        fig,
        "abstract optical penrose triangular moire optical interference pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_penrose_triangular_moire_optical_interference_pattern_black_white_texture()
