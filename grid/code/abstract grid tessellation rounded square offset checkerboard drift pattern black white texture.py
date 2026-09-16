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


def abstract_grid_tessellation_rounded_square_offset_checkerboard_drift_pattern_black_white_texture():
    """Tweak: Grid of rounded squares where alternate rows drift horizontally in opposite directions."""
    fig, ax = setup_ax()
    
    n_rows = 10
    n_cols = 10
    cell_size = 100 / n_cols
    
    for r in range(n_rows):
        # Horizontal drift offset per row
        drift = 4.0 * np.sin(r * 0.5)
        for c in range(n_cols):
            cx = (c + 0.5) * cell_size + drift
            cy = (r + 0.5) * cell_size
            
            w = cell_size * 0.8
            r_c = 0.25 * w
            
            box = FancyBboxPatch(
                (cx - w/2, cy - w/2),
                w,
                w,
                boxstyle=f"round,pad=0,rounding_size={r_c}",
                fill=False,
                edgecolor="black",
                linewidth=1.2,
            )
            ax.add_patch(box)

    save(fig, "abstract grid tessellation rounded square offset checkerboard drift pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_rounded_square_offset_checkerboard_drift_pattern_black_white_texture()
