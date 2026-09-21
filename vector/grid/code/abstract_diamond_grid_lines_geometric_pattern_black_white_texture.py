import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
SCRIPT_DIR = Path(__file__).resolve().parent

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

JPG_DIR = SCRIPT_DIR.parent / "output" / "jpg"
SVG_DIR = SCRIPT_DIR.parent / "output" / "svg"
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
def diamond_grid():
    fig, ax = setup_ax()
    spacing = 6
    for offset in np.arange(-150, 250, spacing):
        lw = 0.8
        ax.plot([offset, offset + 150], [-50, 150], color="black", linewidth=lw)
        ax.plot([offset, offset + 150], [150, -50], color="black", linewidth=lw)
    cx, cy = 50, 50
    for r in np.arange(5, 80, 8):
        theta = np.linspace(0, 2 * np.pi, 5)
        x = cx + r * np.cos(theta)
        y = cy + r * np.sin(theta)
        ax.plot(x, y, color="black", linewidth=1.5)
    save(fig, "diamond_grid")


if __name__ == "__main__":
    diamond_grid()
