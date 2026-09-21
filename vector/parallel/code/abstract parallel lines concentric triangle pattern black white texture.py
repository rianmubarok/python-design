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


def abstract_parallel_lines_concentric_triangle_pattern_black_white_texture():
    """New concept: concentric equilateral triangles, centered"""
    fig, ax = setup_ax()
    n_triangles = 30
    for i in range(n_triangles):
        s = 85 - i * 2.6
        if s <= 0:
            break
        h = s * (3 ** 0.5) / 2
        top = (50, 50 + h * 2 / 3)
        left = (50 - s / 2, 50 - h / 3)
        right = (50 + s / 2, 50 - h / 3)
        ax.plot([top[0], left[0], right[0], top[0]],
                [top[1], left[1], right[1], top[1]],
                color="black", linewidth=0.4)
    save(fig, "abstract parallel lines concentric triangle pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_concentric_triangle_pattern_black_white_texture()
