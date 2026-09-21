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


def abstract_grid_tessellation_triangular_maze_line_offset_pattern_black_white_texture():
    """Tweak: Triangular isometric grid with randomized line segment omissions forming a geometric maze."""
    fig, ax = setup_ax()
    
    a = 8.0  # side length
    h = a * np.sqrt(3) / 2
    
    n_cols = 16
    n_rows = 16
    
    for r in range(n_rows):
        for c in range(n_cols):
            x0 = c * a
            if r % 2 != 0:
                x0 += a / 2
            y0 = r * h
            
            p1 = (x0, y0)
            p2 = (x0 + a, y0)
            p3 = (x0 + a/2, y0 + h)
            
            # Randomly draw triangle edges (omitting ~30% for maze texture)
            if np.random.rand() > 0.3:
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="black", linewidth=1.2)
            if np.random.rand() > 0.3:
                ax.plot([p2[0], p3[0]], [p2[1], p3[1]], color="black", linewidth=1.2)
            if np.random.rand() > 0.3:
                ax.plot([p3[0], p1[0]], [p3[1], p1[1]], color="black", linewidth=1.2)


    all_x = []
    all_y = []
    for line in ax.lines:
        all_x.extend(line.get_xdata())
        all_y.extend(line.get_ydata())
    for patch in ax.patches:
        if hasattr(patch, 'get_patch_transform') and hasattr(patch, 'get_path'):
            trans = patch.get_patch_transform()
            path = patch.get_path()
            vertices = trans.transform_path(path).vertices
            all_x.extend(vertices[:, 0])
            all_y.extend(vertices[:, 1])
        elif hasattr(patch, 'get_path'):
            vertices = patch.get_path().vertices
            all_x.extend(vertices[:, 0])
            all_y.extend(vertices[:, 1])
            
    if all_x and all_y:
        cx = (min(all_x) + max(all_x)) / 2
        cy = (min(all_y) + max(all_y)) / 2
        ax.set_xlim(cx - 55, cx + 55)
        ax.set_ylim(cy - 55, cy + 55)
        
    save(fig, "abstract grid tessellation triangular maze line offset pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_triangular_maze_line_offset_pattern_black_white_texture()
