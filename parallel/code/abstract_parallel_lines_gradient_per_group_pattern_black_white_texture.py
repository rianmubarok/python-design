import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

JPG_DIR = Path("output/jpg")
SVG_DIR = Path("output/svg")
JPG_DIR.mkdir(parents=True, exist_ok=True)
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
    jpg_path = JPG_DIR / f"{name}_{DATE}.jpg"
    svg_path = SVG_DIR / f"{name}_{DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")
def parallel_gradient_group():
    """Garis paralel dengan gradiasi ketebalan per kelompok"""
    fig, ax = setup_ax()

    n_groups = 5
    lines_per_group = 10
    for g in range(n_groups):
        y_start = -5 + g * 22
        for i in range(lines_per_group):
            y = y_start + i * 2
            t = i / lines_per_group
            lw = 0.5 + 4.5 * t
            alpha = 0.4 + 0.6 * t
            ax.plot([-5, 105], [y, y], color="black", linewidth=lw, alpha=alpha)

    save(fig, "parallel_gradient_group")


if __name__ == "__main__":
    parallel_gradient_group()
