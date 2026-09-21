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


def abstract_grid_tessellation_triangular_node_star_burst_radius_pulse_pattern_black_white_texture():
    """Tweak: Triangular grid with 6-point star nodes whose ray count alternates between 6 and 12."""
    fig, ax = setup_ax()
    
    a = 10.0
    h = a * np.sqrt(3) / 2
    
    n_cols = 12
    n_rows = 12
    
    for r in range(n_rows):
        for c in range(n_cols):
            cx = c * a
            if r % 2 != 0:
                cx += a / 2
            cy = r * h
            
            # Ray count alternates
            n_rays = 12 if (r + c) % 2 == 0 else 6
            star_radius = 4.0
            
            for k in range(n_rays):
                angle = k * 2 * np.pi / n_rays
                x_end = cx + star_radius * np.cos(angle)
                y_end = cy + star_radius * np.sin(angle)
                ax.plot([cx, x_end], [cy, y_end], color="black", linewidth=0.8)


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
        
    save(fig, "abstract grid tessellation triangular node star burst radius pulse pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_triangular_node_star_burst_radius_pulse_pattern_black_white_texture()
