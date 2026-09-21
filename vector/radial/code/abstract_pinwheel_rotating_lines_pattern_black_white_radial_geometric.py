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
def pinwheel():
    fig, ax = setup_ax()
    cx, cy = 50, 50
    n_arms = 12
    for i in range(n_arms):
        base_angle = i * (360 / n_arms)
        for j in range(40):
            angle = base_angle + j * 2
            rad = np.radians(angle)
            r_start = j * 1.2
            r_end = r_start + 2
            x1 = cx + r_start * np.cos(rad)
            y1 = cy + r_start * np.sin(rad)
            x2 = cx + r_end * np.cos(np.radians(angle + 3))
            y2 = cy + r_end * np.sin(np.radians(angle + 3))
            lw = 1.0 + 1.5 * (j / 40)
            ax.plot([x1, x2], [y1, y2], color="black", linewidth=lw)
    ax.plot(cx, cy, "o", color="black", markersize=12)
    save(fig, "pinwheel")


if __name__ == "__main__":
    pinwheel()
