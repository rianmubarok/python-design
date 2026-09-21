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


def abstract_geometric_concentric_polygon_morph_pattern_black_white_texture():
    """Tweak: Concentric regular polygons morphing from 3 sides to 12 sides towards center."""
    fig, ax = setup_ax()
    
    n_poly = 30
    for i in range(n_poly):
        r = 48 - i * 1.5
        if r <= 2:
            break
            
        # Number of vertices morphs from 3 (triangle) to 12 (dodecagon)
        n_sides = int(3 + 9 * (i / n_poly))
        lw = 0.5 + 0.4 * (1 - i / n_poly)
        
        poly = RegularPolygon((50, 50), numVertices=n_sides, radius=r, orientation=i*0.1, fill=False, edgecolor="black", linewidth=lw)
        ax.add_patch(poly)

    save(fig, "abstract geometric concentric polygon morph pattern black white texture")


if __name__ == "__main__":
    abstract_geometric_concentric_polygon_morph_pattern_black_white_texture()
