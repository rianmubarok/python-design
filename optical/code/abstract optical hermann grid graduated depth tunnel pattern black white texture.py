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


def generate():
    """Hermann grid with graduated block sizes — shrinks toward center, creating depth tunnel."""
    fig, ax = setup_ax()

    n = 10
    cx, cy = 50, 50

    for r in range(n):
        for c in range(n):
            grid_x = c * 10.0 + 2.5
            grid_y = r * 10.0 + 2.5

            dist = np.sqrt((grid_x + 3.5 - cx)**2 + (grid_y + 3.5 - cy)**2)
            scale = 0.4 + 0.6 * (dist / 50.0)
            block_w = 7.0 * scale
            gap_offset = (7.0 - block_w) / 2

            rect = Rectangle(
                (grid_x + gap_offset, grid_y + gap_offset),
                block_w, block_w,
                facecolor="black", edgecolor="black"
            )
            ax.add_patch(rect)

    save(fig, "abstract optical hermann grid graduated depth tunnel pattern black white texture")


if __name__ == "__main__":
    generate()
