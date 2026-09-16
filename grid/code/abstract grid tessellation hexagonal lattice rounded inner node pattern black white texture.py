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


def abstract_grid_tessellation_hexagonal_lattice_rounded_inner_node_pattern_black_white_texture():
    """Tweak: Hexagonal grid with nested inner scaling hexagons in every cell."""
    fig, ax = setup_ax()
    
    r_outer = 6.0
    dx = r_outer * np.sqrt(3)
    dy = r_outer * 1.5
    
    n_cols = 12
    n_rows = 12
    
    for row in range(n_rows):
        for col in range(n_cols):
            cx = col * dx
            if row % 2 != 0:
                cx += dx / 2
            cy = row * dy
            
            # Outer hexagon
            hex_out = RegularPolygon((cx, cy), numVertices=6, radius=r_outer, orientation=0, fill=False, edgecolor="black", linewidth=1.2)
            ax.add_patch(hex_out)
            
            # Concentric inner hexagons scaling down
            for scale in [0.75, 0.5, 0.25]:
                hex_in = RegularPolygon((cx, cy), numVertices=6, radius=r_outer*scale, orientation=0, fill=False, edgecolor="black", linewidth=0.6)
                ax.add_patch(hex_in)

    save(fig, "abstract grid tessellation hexagonal lattice rounded inner node pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_hexagonal_lattice_rounded_inner_node_pattern_black_white_texture()
