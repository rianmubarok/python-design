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
    Truchet Tiles.
    A maze-like abstract grid created using quarter-circle Truchet tiles
    that are randomly rotated.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.patches as patches
    
    cell_size = 4.0
    cols = int(120 / cell_size) + 1
    rows = int(120 / cell_size) + 1

    for row in range(-2, rows):
        for col in range(-2, cols):
            x = col * cell_size
            y = row * cell_size
            
            # A Truchet tile has two quarter circles.
            # State 0: top-left and bottom-right corners
            # State 1: top-right and bottom-left corners
            state = rng.choice([0, 1])
            
            if state == 0:
                c1 = patches.Arc((x, y + cell_size), cell_size, cell_size, 
                                 angle=270, theta1=0, theta2=90, 
                                 linewidth=4.0, color="black", capstyle="round")
                c2 = patches.Arc((x + cell_size, y), cell_size, cell_size, 
                                 angle=90, theta1=0, theta2=90, 
                                 linewidth=4.0, color="black", capstyle="round")
            else:
                c1 = patches.Arc((x, y), cell_size, cell_size, 
                                 angle=0, theta1=0, theta2=90, 
                                 linewidth=4.0, color="black", capstyle="round")
                c2 = patches.Arc((x + cell_size, y + cell_size), cell_size, cell_size, 
                                 angle=180, theta1=0, theta2=90, 
                                 linewidth=4.0, color="black", capstyle="round")
                                 
            ax.add_patch(c1)
            ax.add_patch(c2)

    save(fig, "abstract grid tessellation quarter circle truchet tile pattern black white texture")


if __name__ == "__main__":
    draw()
