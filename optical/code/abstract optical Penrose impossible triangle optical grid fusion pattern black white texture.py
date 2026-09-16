import numpy as np
import matplotlib.pyplot as plt
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
    ax.set_xlim(-10, 110)
    ax.set_ylim(-10, 110)
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


def abstract_optical_Penrose_impossible_triangle_optical_grid_fusion_pattern_black_white_texture():
    """Wild Combination: Penrose impossible triangle paradox wireframe with parallel line shading!"""
    fig, ax = setup_ax()
    
    # Vertices of Penrose impossible triangle tribar
    p1 = (50, 85)
    p2 = (15, 20)
    p3 = (85, 20)
    
    # Inner offset vertices
    offset = 12.0
    p1_in = (50, 85 - offset)
    p2_in = (15 + offset*0.866, 20 + offset*0.5)
    p3_in = (85 - offset*0.866, 20 + offset*0.5)
    
    # Draw outer and inner triangles
    ax.plot([p1[0], p2[0], p3[0], p1[0]], [p1[1], p2[1], p3[1], p1[1]], color="black", linewidth=1.5)
    ax.plot([p1_in[0], p2_in[0], p3_in[0], p1_in[0]], [p1_in[1], p2_in[1], p3_in[1], p1_in[1]], color="black", linewidth=1.5)
    
    # Connect corners for 3D impossible beam overlaps
    ax.plot([p1[0], p1_in[0]], [p1[1], p1_in[1]], color="black", linewidth=1.5)
    ax.plot([p2[0], p2_in[0]], [p2[1], p2_in[1]], color="black", linewidth=1.5)
    ax.plot([p3[0], p3_in[0]], [p3[1], p3_in[1]], color="black", linewidth=1.5)
    
    # Parallel line hatchings inside beam faces
    for t in np.linspace(0.1, 0.9, 15):
        lx1 = p1[0] + t * (p2[0] - p1[0])
        ly1 = p1[1] + t * (p2[1] - p1[1])
        lx2 = p1_in[0] + t * (p2_in[0] - p1_in[0])
        ly2 = p1_in[1] + t * (p2_in[1] - p1_in[1])
        ax.plot([lx1, lx2], [ly1, ly2], color="black", linewidth=0.6)

    save(fig, "abstract optical Penrose impossible triangle optical grid fusion pattern black white texture")


if __name__ == "__main__":
    abstract_optical_Penrose_impossible_triangle_optical_grid_fusion_pattern_black_white_texture()
