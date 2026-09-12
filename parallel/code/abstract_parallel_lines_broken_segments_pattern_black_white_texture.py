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
def parallel_broken():
    """Garis paralel dengan potongan/patahan teratur"""
    fig, ax = setup_ax()

    n_lines = 45
    for i in range(n_lines):
        y = -5 + i * 2.4
        segments = []
        x = -5
        while x < 105:
            seg_len = np.random.uniform(15, 35)
            x_end = min(x + seg_len, 105)
            segments.append((x, x_end))
            x = x_end + np.random.uniform(10, 20)
        lw = np.random.choice([2.0, 3.0, 4.0])
        for x1, x2 in segments:
            ax.plot([x1, x2], [y, y], color="black", linewidth=lw)

    save(fig, "parallel_broken")


if __name__ == "__main__":
    parallel_broken()
