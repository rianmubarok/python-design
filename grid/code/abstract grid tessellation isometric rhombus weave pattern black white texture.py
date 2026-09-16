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


def abstract_grid_tessellation_isometric_rhombus_weave_pattern_black_white_texture():
    """Tweak: Isometric Rhombus Grid with inner parallel line hatchings."""
    fig, ax = setup_ax()
    
    a = 10.0
    h = a * np.sqrt(3) / 2
    
    n_cols = 12
    n_rows = 12
    
    for r in range(n_rows):
        for c in range(n_cols):
            cx = c * a * 1.5
            cy = r * h * 2
            if c % 2 != 0:
                cy += h
                
            # Rhombus vertices
            v0 = (cx, cy)
            v1 = (cx + a/2, cy + h)
            v2 = (cx + a * 1.5, cy + h)
            v3 = (cx + a, cy)
            
            # Outer boundary
            ax.plot([v0[0], v1[0], v2[0], v3[0], v0[0]], [v0[1], v1[1], v2[1], v3[1], v0[1]], color="black", linewidth=1.2)
            
            # Inner parallel hatchings
            n_hatch = 5
            for k in range(1, n_hatch):
                t = k / n_hatch
                p_start = (v0[0] + t * (v1[0] - v0[0]), v0[1] + t * (v1[1] - v0[1]))
                p_end = (v3[0] + t * (v2[0] - v3[0]), v3[1] + t * (v2[1] - v3[1]))
                ax.plot([p_start[0], p_end[0]], [p_start[1], p_end[1]], color="black", linewidth=0.6)


    all_x = []
    all_y = []
    for line in ax.lines:
        all_x.extend(line.get_xdata())
        all_y.extend(line.get_ydata())
    for patch in ax.patches:
        if hasattr(patch, 'get_path'):
            vertices = patch.get_path().vertices
            all_x.extend(vertices[:, 0])
            all_y.extend(vertices[:, 1])
            
    if all_x and all_y:
        cx = (min(all_x) + max(all_x)) / 2
        cy = (min(all_y) + max(all_y)) / 2
        ax.set_xlim(cx - 55, cx + 55)
        ax.set_ylim(cy - 55, cy + 55)
        
    save(fig, "abstract grid tessellation isometric rhombus weave pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_isometric_rhombus_weave_pattern_black_white_texture()
