import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
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
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
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


def abstract_optical_cafe_wall_illusion_grid_pattern_black_white_texture():
    """Tweak: Café Wall optical illusion with staggered checkerboard rows causing lines to appear tilted."""
    fig, ax = setup_ax()
    
    n_rows = 12
    n_cols = 12
    row_h = 100 / n_rows
    col_w = 100 / n_cols
    
    # Offsets for each row to trigger the illusion
    offsets = [0, 0.25, 0.5, 0.25, 0, -0.25, -0.5, -0.25, 0, 0.25, 0.5, 0.25]
    
    for r in range(n_rows):
        y = r * row_h
        shift = offsets[r % len(offsets)] * col_w
        
        for c in range(-1, n_cols + 2):
            if (c + r) % 2 == 0:
                rect = Rectangle((c * col_w + shift, y), col_w, row_h, fill=True, facecolor="black")
                ax.add_patch(rect)
                
        # Thin mortar line between rows
        ax.plot([0, 100], [y, y], color="black", linewidth=1.5)

    save(fig, "abstract optical cafe wall illusion grid pattern black white texture")


if __name__ == "__main__":
    abstract_optical_cafe_wall_illusion_grid_pattern_black_white_texture()
