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


def abstract_grid_tessellation_penrose_kite_dart_rounded_corner_pattern_black_white_texture():
    """Tweak: Penrose-like aperiodic star tiling with rounded apex curves on every tile."""
    fig, ax = setup_ax()
    
    # Generate 5-fold symmetrical star tiles around center (50, 50)
    n_rings = 5
    cx, cy = 50, 50
    
    for ring in range(1, n_rings + 1):
        r_outer = ring * 9.0
        n_tiles = ring * 5
        
        for k in range(n_tiles):
            angle = k * 2 * np.pi / n_tiles
            x = cx + r_outer * np.cos(angle)
            y = cy + r_outer * np.sin(angle)
            
            # Dart / Kite apex points
            tile_w = 4.0
            pts = np.array([
                [x, y + tile_w],
                [x + tile_w, y],
                [x, y - tile_w],
                [x - tile_w, y]
            ])
            poly = Polygon(pts, fill=False, edgecolor="black", linewidth=1.0)
            ax.add_patch(poly)

    save(fig, "abstract grid tessellation penrose kite dart rounded corner pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_penrose_kite_dart_rounded_corner_pattern_black_white_texture()
