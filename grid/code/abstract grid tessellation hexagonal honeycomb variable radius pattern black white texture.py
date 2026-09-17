import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
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
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
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


def abstract_grid_tessellation_hexagonal_honeycomb_variable_radius_pattern_black_white_texture():
    """Tweak: Hexagonal grid where cell radius shrinks dynamically toward the center of the canvas."""
    fig, ax = setup_ax()

    r_max = 6.0
    dx = r_max * np.sqrt(3)
    dy = r_max * 1.5

    # Build the lattice centered on the canvas (50, 50) so the shrink focal point
    # and the artwork itself are both perfectly centered.
    n = 7
    cells = []
    for row in range(-n, n + 1):
        for col in range(-n, n + 1):
            cx = 50 + col * dx
            if row % 2 != 0:
                cx += dx / 2
            cy = 50 + row * dy
            cells.append((cx, cy))

    max_dist = max(np.hypot(cx - 50, cy - 50) for cx, cy in cells)

    for cx, cy in cells:
        dist = np.hypot(cx - 50, cy - 50)
        r_cell = r_max * (0.35 + 0.65 * (dist / max_dist))
        r_cell = min(r_max, max(1.0, r_cell))

        hex_cell = RegularPolygon((cx, cy), numVertices=6, radius=r_cell, orientation=0, fill=False, edgecolor="black", linewidth=1.2)
        ax.add_patch(hex_cell)

    save(fig, "abstract grid tessellation hexagonal honeycomb variable radius pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_hexagonal_honeycomb_variable_radius_pattern_black_white_texture()
