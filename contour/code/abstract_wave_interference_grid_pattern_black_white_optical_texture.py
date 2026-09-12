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
def wave_interference_grid():
    fig, ax = setup_ax()
    x = np.linspace(-5, 105, 400)
    y = np.linspace(-5, 105, 400)
    X, Y = np.meshgrid(x, y)
    Z1 = np.sin(X * 0.3) * np.cos(Y * 0.3)
    Z2 = np.cos(X * 0.3) * np.sin(Y * 0.3)
    Z = Z1 + Z2
    n_levels = 25
    levels = np.linspace(Z.min(), Z.max(), n_levels)
    ax.contour(X, Y, Z, levels=levels, colors='black', linewidths=0.7)
    save(fig, "wave_interference_grid")


if __name__ == "__main__":
    wave_interference_grid()
