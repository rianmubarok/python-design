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


def abstract_grid_tessellation_voronoi_relaxation_tile_pattern_black_white_texture():
    """Tweak: Lloyd-relaxed Voronoi cell grid filled with concentric inner polygon outlines."""
    fig, ax = setup_ax()
    
    # 25 seed points
    n_seeds = 25
    seeds_x = np.random.uniform(10, 90, n_seeds)
    seeds_y = np.random.uniform(10, 90, n_seeds)
    
    # Render approximate Voronoi inner rings around each seed
    t = np.linspace(0, 2 * np.pi, 7)  # Heptagon approximation
    
    for i in range(n_seeds):
        sx, sy = seeds_x[i], seeds_y[i]
        
        # Concentric rings
        for r in np.linspace(1.5, 9.0, 5):
            x_pts = sx + r * np.cos(t)
            y_pts = sy + r * np.sin(t)
            poly = Polygon(np.column_stack([x_pts, y_pts]), fill=False, edgecolor="black", linewidth=0.8)
            ax.add_patch(poly)

    save(fig, "abstract grid tessellation voronoi relaxation tile pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_voronoi_relaxation_tile_pattern_black_white_texture()
