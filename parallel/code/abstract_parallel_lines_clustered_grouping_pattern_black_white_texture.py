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
def parallel_clustered():
    """Garis paralel berkelompok (cluster)"""
    fig, ax = setup_ax()

    y = -5
    group_idx = 0
    while y < 105:
        group_size = np.random.choice([2, 3, 4, 5])
        group_spacing = np.random.uniform(1.0, 1.8)
        group_gap = np.random.uniform(4, 8)

        for j in range(group_size):
            lw = np.random.choice([1.5, 2.0, 2.5, 3.0])
            ax.plot([-5, 105], [y, y], color="black", linewidth=lw)
            y += group_spacing

        y += group_gap
        group_idx += 1

    save(fig, "parallel_clustered")


if __name__ == "__main__":
    parallel_clustered()
