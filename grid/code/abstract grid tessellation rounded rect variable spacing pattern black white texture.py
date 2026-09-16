import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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


def abstract_grid_tessellation_rounded_rect_variable_spacing_pattern_black_white_texture():
    """Tweak: Grid of rounded rectangles with dynamically modulating cell sizes and spacing."""
    fig, ax = setup_ax()
    
    n_cols = 12
    n_rows = 12
    
    # Non-linear cell positions
    x_positions = np.linspace(0, 100, n_cols + 1)
    x_positions += 3 * np.sin(x_positions * 0.1)
    
    y_positions = np.linspace(0, 100, n_rows + 1)
    y_positions += 3 * np.cos(y_positions * 0.1)
    
    for i in range(n_cols):
        for j in range(n_rows):
            x1, x2 = x_positions[i], x_positions[i+1]
            y1, y2 = y_positions[j], y_positions[j+1]
            
            w = (x2 - x1) * 0.82
            h = (y2 - y1) * 0.82
            
            if w <= 1 or h <= 1:
                continue
                
            r = 0.25 * min(w, h)
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            
            box = FancyBboxPatch(
                (cx - w/2, cy - h/2),
                w,
                h,
                boxstyle=f"round,pad=0,rounding_size={r}",
                fill=False,
                edgecolor="black",
                linewidth=1.2,
            )
            ax.add_patch(box)

    save(fig, "abstract grid tessellation rounded rect variable spacing pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_rounded_rect_variable_spacing_pattern_black_white_texture()
