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


def abstract_parallel_lines_mosaic_pattern_black_white_texture():
    fig, ax = setup_ax()
    block_size = 10
    for bx in range(-5, 105, block_size):
        for by in range(-5, 105, block_size):
            direction = ((bx // block_size) + (by // block_size)) % 2
            lw = 0.4 + 0.3 * np.sin(bx * 0.1 + by * 0.1)
            if direction == 0:
                for i in range(3):
                    y = by + 2 + i * 3
                    ax.plot([bx, bx + block_size], [y, y], color="black", linewidth=lw)
            else:
                for i in range(3):
                    x = bx + 2 + i * 3
                    ax.plot([x, x], [by, by + block_size], color="black", linewidth=lw)
    save(fig, "abstract parallel lines mosaic pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_mosaic_pattern_black_white_texture()
