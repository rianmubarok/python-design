import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, FancyBboxPatch
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


def abstract_grid_tessellation_octagonal_square_interlocking_node_pattern_black_white_texture():
    """Tweak: Octagonal and square semiregular grid with concentric inner rounded nodes."""
    fig, ax = setup_ax()
    
    r_oct = 6.0
    dx = r_oct * 2.4
    dy = r_oct * 2.4
    
    n_cols = 8
    n_rows = 8
    
    for r in range(n_rows):
        for c in range(n_cols):
            cx = (c + 0.5) * dx
            cy = (r + 0.5) * dy
            
            # Octagon
            oct_patch = RegularPolygon((cx, cy), numVertices=8, radius=r_oct, orientation=np.pi/8, fill=False, edgecolor="black", linewidth=1.2)
            ax.add_patch(oct_patch)
            
            # Inner concentric rounded octagons
            for scale in [0.7, 0.4]:
                oct_in = RegularPolygon((cx, cy), numVertices=8, radius=r_oct*scale, orientation=np.pi/8, fill=False, edgecolor="black", linewidth=0.6)
                ax.add_patch(oct_in)
                
            # Interlocking square at corner nodes
            sq_w = 4.0
            sq_box = FancyBboxPatch((cx + dx/2 - sq_w/2, cy + dy/2 - sq_w/2), sq_w, sq_w, boxstyle="round,pad=0,rounding_size=0.8", fill=False, edgecolor="black", linewidth=1.0)
            ax.add_patch(sq_box)


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
        
    save(fig, "abstract grid tessellation octagonal square interlocking node pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_octagonal_square_interlocking_node_pattern_black_white_texture()
