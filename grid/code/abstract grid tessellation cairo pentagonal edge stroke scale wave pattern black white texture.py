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


def abstract_grid_tessellation_cairo_pentagonal_edge_stroke_scale_wave_pattern_black_white_texture():
    """Tweak: Cairo pentagons with linewidths scaling based on cell distance to center."""
    fig, ax = setup_ax()
    
    a = 12.0
    n_cols = 10
    n_rows = 10
    
    for r in range(n_rows):
        for c in range(n_cols):
            cx = c * a
            cy = r * a
            
            # Distance from center
            dist = np.sqrt((cx - 50)**2 + (cy - 50)**2)
            lw = 0.4 + 2.2 * np.exp(-dist * 0.03)
            
            pts = np.array([
                [cx, cy],
                [cx + a/2, cy - a/4],
                [cx + a, cy],
                [cx + 3*a/4, cy + a],
                [cx + a/4, cy + a]
            ])
            
            poly = Polygon(pts, fill=False, edgecolor="black", linewidth=lw)
            ax.add_patch(poly)

    save(fig, "abstract grid tessellation cairo pentagonal edge stroke scale wave pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_cairo_pentagonal_edge_stroke_scale_wave_pattern_black_white_texture()
