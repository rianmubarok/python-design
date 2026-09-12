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


def abstract_parallel_lines_dashed_pattern_black_white_texture():
    """Garis paralel putus-putus teratur"""
    fig, ax = setup_ax()
    n_lines = 45
    dash_len = 5
    gap_len = 3
    for i in range(n_lines):
        y = -5 + i * 2.4
        x = -5
        lw = np.random.choice([2.0, 3.0, 4.0])
        while x < 105:
            x_end = min(x + dash_len, 105)
            ax.plot([x, x_end], [y, y], color="black", linewidth=lw)
            x = x_end + gap_len
    save(fig, "abstract_parallel_lines_dashed_pattern_black_white_texture")


if __name__ == "__main__":
    abstract_parallel_lines_dashed_pattern_black_white_texture()
