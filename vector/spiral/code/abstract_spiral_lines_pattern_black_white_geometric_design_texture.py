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
def spiral():
    fig, ax = setup_ax()
    cx, cy = 50, 50
    theta = np.linspace(0, 12 * np.pi, 1000)
    r = 1 + theta * 1.5
    x = cx + r * np.cos(theta)
    y = cy + r * np.sin(theta)
    for i in range(len(x) - 1):
        dist = np.sqrt((x[i] - cx)**2 + (y[i] - cy)**2)
        lw = 1.0 + 3.0 * (1 - dist / 80)
        lw = max(0.5, min(lw, 4.0))
        ax.plot([x[i], x[i+1]], [y[i], y[i+1]], color="black", linewidth=lw)
    ax.plot(cx, cy, "o", color="black", markersize=15)
    save(fig, "spiral")


if __name__ == "__main__":
    spiral()
