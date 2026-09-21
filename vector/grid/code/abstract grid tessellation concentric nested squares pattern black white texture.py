import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


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


def draw():
    """
    Concentric Nested Squares Grid.
    A grid where every cell contains a series of shrinking nested squares,
    resembling a highly detailed architectural floor plan or optical illusion.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.patches as patches

    cell_size = 15.0
    cols = int(120 / cell_size) + 1
    rows = int(120 / cell_size) + 1
    
    for row in range(-1, rows):
        for col in range(-1, cols):
            cx = col * cell_size + cell_size / 2
            cy = row * cell_size + cell_size / 2
            
            # Randomize the number of nested squares for each cell
            n_nests = rng.integers(3, 12)
            
            for i in range(n_nests):
                # Shrink size
                s = cell_size * (1.0 - i / n_nests)
                
                # Offset slightly towards the center to avoid perfectly centered nests
                # for an op-art look
                shift_x = (rng.random() - 0.5) * 1.5 * (i / n_nests)
                shift_y = (rng.random() - 0.5) * 1.5 * (i / n_nests)
                
                rect = patches.Rectangle((cx - s/2 + shift_x, cy - s/2 + shift_y), s, s, 
                                         linewidth=1.2, edgecolor='black', facecolor='none')
                ax.add_patch(rect)

    save(fig, "abstract grid tessellation concentric nested squares pattern black white texture")


if __name__ == "__main__":
    draw()
