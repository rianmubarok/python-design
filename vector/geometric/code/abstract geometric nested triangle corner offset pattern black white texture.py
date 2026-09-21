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


def abstract_geometric_nested_triangle_corner_offset_pattern_black_white_texture():
    """Tweak: Nested triangles where each inner triangle rotates and shifts towards a top corner."""
    fig, ax = setup_ax()
    
    n_triangles = 30
    for i in range(n_triangles):
        r = 50 - i * 1.5
        if r <= 2:
            break
            
        # Rotating angle and top corner shift
        angle = i * 0.1
        shift_y = i * 0.5
        
        t_vals = np.array([0, 2*np.pi/3, 4*np.pi/3]) + angle
        x = 50 + r * np.cos(t_vals)
        y = 50 + shift_y + r * np.sin(t_vals)
        
        poly = Polygon(np.column_stack([x, y]), fill=False, edgecolor="black", linewidth=0.8)
        ax.add_patch(poly)

    save(fig, "abstract geometric nested triangle corner offset pattern black white texture")


if __name__ == "__main__":
    abstract_geometric_nested_triangle_corner_offset_pattern_black_white_texture()
