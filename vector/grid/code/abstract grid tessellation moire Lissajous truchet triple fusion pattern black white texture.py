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


def abstract_grid_tessellation_moire_Lissajous_truchet_triple_fusion_pattern_black_white_texture():
    """Wild Combination: Triple fusion of Isometric grid + Lissajous curves + Moire offset overlay."""
    fig, ax = setup_ax()
    
    n_cols = 8
    n_rows = 8
    cell_size = 100 / n_cols
    t = np.linspace(0, 2 * np.pi, 300)
    
    # Layer 1: Base Lissajous grid
    for r in range(n_rows):
        for c in range(n_cols):
            cx = (c + 0.5) * cell_size
            cy = (r + 0.5) * cell_size
            
            x = cx + (cell_size * 0.42) * np.sin((r + 1) * t)
            y = cy + (cell_size * 0.42) * np.cos((c + 1) * t)
            ax.plot(x, y, color="black", linewidth=1.0)

    # Layer 2: Offset Moire Lissajous overlay
    offset = 1.8
    for r in range(n_rows):
        for c in range(n_cols):
            cx = (c + 0.5) * cell_size + offset
            cy = (r + 0.5) * cell_size + offset
            
            x = cx + (cell_size * 0.42) * np.sin((r + 1) * t)
            y = cy + (cell_size * 0.42) * np.cos((c + 1) * t)
            ax.plot(x, y, color="black", linewidth=0.8, alpha=0.7)

    save(fig, "abstract grid tessellation moire Lissajous truchet triple fusion pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_moire_Lissajous_truchet_triple_fusion_pattern_black_white_texture()
