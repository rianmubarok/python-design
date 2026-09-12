import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

SIZE = 4000
DPI = 300
SEED = 42

PNG_DIR = Path("output/png")
SVG_DIR = Path("output/svg")
PNG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    png_path = PNG_DIR / f"{name}.png"
    svg_path = SVG_DIR / f"{name}.svg"
    fig.savefig(png_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {png_path} | {svg_path}")


def abstract_parallel_lines_nested_rectangle_pattern_black_white_texture():
    """Garis paralel membentuk persegi bersarang"""
    fig, ax = setup_ax()
    cx, cy = 50, 50
    n_rects = 25
    for i in range(n_rects):
        size = 5 + i * 3.5
        lw = 1.0 + 2.0 * (i / n_rects)
        rect = plt.Rectangle((cx - size, cy - size), size * 2, size * 2,
                              fill=False, edgecolor='black', linewidth=lw)
        ax.add_patch(rect)
    save(fig, "abstract_parallel_lines_nested_rectangle_pattern_black_white_texture")


if __name__ == "__main__":
    abstract_parallel_lines_nested_rectangle_pattern_black_white_texture()
