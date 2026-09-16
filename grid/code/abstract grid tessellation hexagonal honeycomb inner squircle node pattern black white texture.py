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


def abstract_grid_tessellation_hexagonal_honeycomb_inner_squircle_node_pattern_black_white_texture():
    """Tweak: Hexagonal honeycomb containing inner squircle nodes scaling down."""
    fig, ax = setup_ax()
    
    r_outer = 6.0
    dx = r_outer * np.sqrt(3)
    dy = r_outer * 1.5
    
    n_cols = 12
    n_rows = 12
    t_vals = np.linspace(0, 2 * np.pi, 100)
    
    for row in range(n_rows):
        for col in range(n_cols):
            cx = col * dx
            if row % 2 != 0:
                cx += dx / 2
            cy = row * dy
            
            # Outer hexagon
            hex_out = RegularPolygon((cx, cy), numVertices=6, radius=r_outer, orientation=0, fill=False, edgecolor="black", linewidth=1.2)
            ax.add_patch(hex_out)
            
            # Inner squircle node
            r_sq = r_outer * 0.5
            p = 3.5
            cos_t = np.cos(t_vals)
            sin_t = np.sin(t_vals)
            x_sq = cx + r_sq * np.sign(cos_t) * (np.abs(cos_t) ** (2 / p))
            y_sq = cy + r_sq * np.sign(sin_t) * (np.abs(sin_t) ** (2 / p))
            ax.plot(x_sq, y_sq, color="black", linewidth=0.8)


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
        
    save(fig, "abstract grid tessellation hexagonal honeycomb inner squircle node pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_hexagonal_honeycomb_inner_squircle_node_pattern_black_white_texture()
