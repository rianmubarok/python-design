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


def abstract_parallel_lines_gradient_angular_pattern_black_white_texture():
    """Garis paralel dengan gradiasi sudut"""
    fig, ax = setup_ax()
    n_lines = 50
    for i in range(n_lines):
        y = -5 + i * 2.2
        angle = -15 + 30 * (i / n_lines)
        rad = np.radians(angle)
        length = 110
        x_center = 50
        x1 = x_center - length * np.cos(rad) / 2
        x2 = x_center + length * np.cos(rad) / 2
        y1 = y - length * np.sin(rad) / 2
        y2 = y + length * np.sin(rad) / 2
        lw = 1.5 + 2.0 * np.abs(np.sin(i * 0.2))
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=lw)
    save(fig, "abstract_parallel_lines_gradient_angular_pattern_black_white_texture")


if __name__ == "__main__":
    abstract_parallel_lines_gradient_angular_pattern_black_white_texture()
