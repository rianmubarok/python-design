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


def fractal_tree():
    fig, ax = setup_ax()
    def draw_branch(x, y, angle, length, depth, lw):
        if depth == 0 or length < 1:
            return
        x2 = x + length * np.cos(np.radians(angle))
        y2 = y + length * np.sin(np.radians(angle))
        ax.plot([x, x2], [y, y2], color="black", linewidth=lw)
        draw_branch(x2, y2, angle - 25, length * 0.7, depth - 1, lw * 0.8)
        draw_branch(x2, y2, angle + 25, length * 0.7, depth - 1, lw * 0.8)
    draw_branch(50, 5, 90, 25, 8, 3.0)
    save(fig, "fractal_tree")


if __name__ == "__main__":
    fractal_tree()
