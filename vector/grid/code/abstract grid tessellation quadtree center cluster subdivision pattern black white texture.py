import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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


def abstract_grid_tessellation_quadtree_center_cluster_subdivision_pattern_black_white_texture():
    """Tweak: Quadtree grid that subdivides densely near canvas center and stays coarse at edges."""
    fig, ax = setup_ax()

    def subdivide(x, y, size, depth, max_depth):
        cx, cy = x + size/2, y + size/2
        dist_center = np.sqrt((cx - 50)**2 + (cy - 50)**2)
        
        # Dense near center
        should_split = dist_center < 35 or depth < 2
        
        w = size * 0.94
        r_c = 0.2 * w
        box = FancyBboxPatch((x + (size-w)/2, y + (size-w)/2), w, w, boxstyle=f"round,pad=0,rounding_size={r_c}", fill=False, edgecolor="black", linewidth=0.6 + 0.3*(max_depth-depth))
        ax.add_patch(box)
        
        if depth < max_depth and should_split:
            half = size / 2
            subdivide(x, y, half, depth + 1, max_depth)
            subdivide(x + half, y, half, depth + 1, max_depth)
            subdivide(x, y + half, half, depth + 1, max_depth)
            subdivide(x + half, y + half, half, depth + 1, max_depth)

    subdivide(0, 0, 100, 0, 4)

    save(fig, "abstract grid tessellation quadtree center cluster subdivision pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_quadtree_center_cluster_subdivision_pattern_black_white_texture()
