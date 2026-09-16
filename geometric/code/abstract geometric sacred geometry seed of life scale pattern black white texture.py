import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
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


def abstract_geometric_sacred_geometry_seed_of_life_scale_pattern_black_white_texture():
    """Tweak: Seed of Life overlapping geometric circles with varying line weights."""
    fig, ax = setup_ax()
    
    r_circle = 20.0
    cx, cy = 50, 50
    
    # Center circle
    circ0 = Circle((cx, cy), r_circle, fill=False, edgecolor="black", linewidth=1.5)
    ax.add_patch(circ0)
    
    # 6 surrounding Seed of Life circles
    for i in range(6):
        angle = i * np.pi / 3
        x_c = cx + r_circle * np.cos(angle)
        y_c = cy + r_circle * np.sin(angle)
        
        for scale in [1.0, 0.75, 0.5]:
            circ = Circle((x_c, y_c), r_circle * scale, fill=False, edgecolor="black", linewidth=1.0 if scale==1.0 else 0.6)
            ax.add_patch(circ)
            
    # Bounding outer ring
    outer_circ = Circle((cx, cy), 2 * r_circle, fill=False, edgecolor="black", linewidth=2.0)
    ax.add_patch(outer_circ)

    save(fig, "abstract geometric sacred geometry seed of life scale pattern black white texture")


if __name__ == "__main__":
    abstract_geometric_sacred_geometry_seed_of_life_scale_pattern_black_white_texture()
