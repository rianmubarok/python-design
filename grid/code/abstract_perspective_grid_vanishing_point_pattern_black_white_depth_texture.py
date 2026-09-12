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
def perspective_grid():
    fig, ax = setup_ax()
    vx, vy = 50, 90
    n_lines_h = 15
    n_lines_v = 20
    for i in range(n_lines_h):
        y = -5 + i * 7
        ax.plot([-5, 105], [y, y], color="black", linewidth=0.8)
    for i in range(n_lines_v):
        x = -5 + i * 5.5
        ax.plot([x, vx], [-5, vy], color="black", linewidth=0.8)
        ax.plot([x, vx], [105, vy], color="black", linewidth=0.8)
    ax.plot(vx, vy, "o", color="black", markersize=10)
    save(fig, "perspective_grid")


if __name__ == "__main__":
    perspective_grid()
