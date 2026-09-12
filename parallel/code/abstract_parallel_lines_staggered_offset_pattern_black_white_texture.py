import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

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
    png_path = PNG_DIR / f"{name}_{DATE}.png"
    svg_path = SVG_DIR / f"{name}_{DATE}.svg"
    fig.savefig(png_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {png_path} | {svg_path}")
def parallel_staggered():
    """Garis paralel dengan offset/stagger teratur"""
    fig, ax = setup_ax()

    n_lines = 40
    stagger_amp = 8
    for i in range(n_lines):
        y = -5 + i * 2.8
        x_offset = stagger_amp * np.sin(i * 0.8)
        lw = 2.0 + 1.5 * np.abs(np.sin(i * 0.4))
        ax.plot([-5 + x_offset, 105 + x_offset], [y, y], color="black", linewidth=lw)

    save(fig, "parallel_staggered")


if __name__ == "__main__":
    parallel_staggered()
