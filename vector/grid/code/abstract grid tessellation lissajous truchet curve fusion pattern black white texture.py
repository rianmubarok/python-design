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


def abstract_grid_tessellation_lissajous_truchet_curve_fusion_pattern_black_white_texture():
    """Wild Combo: Grid of cells where each cell renders a Lissajous curve connecting cell midpoints."""
    fig, ax = setup_ax()
    
    n = 6
    cell_size = 100 / n
    t = np.linspace(0, 2 * np.pi, 400)
    
    for r in range(n):
        for c in range(n):
            cx = (c + 0.5) * cell_size
            cy = (r + 0.5) * cell_size
            
            # Harmonically tuned Lissajous parameters per cell
            freq_x = r + 1
            freq_y = c + 2
            phase = (r * c) * np.pi / 4
            
            x = cx + (cell_size * 0.4) * np.sin(freq_x * t + phase)
            y = cy + (cell_size * 0.4) * np.sin(freq_y * t)
            
            ax.plot(x, y, color="black", linewidth=1.2)
            
            # Tile boundary box
            ax.plot([cx - cell_size/2, cx + cell_size/2, cx + cell_size/2, cx - cell_size/2, cx - cell_size/2],
                    [cy - cell_size/2, cy - cell_size/2, cy + cell_size/2, cy + cell_size/2, cy - cell_size/2],
                    color="black", linewidth=0.5, alpha=0.4)

    save(fig, "abstract grid tessellation lissajous truchet curve fusion pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_lissajous_truchet_curve_fusion_pattern_black_white_texture()
