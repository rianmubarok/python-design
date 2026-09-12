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
def converging_perspective():
    fig, ax = setup_ax()
    focus_x, focus_y = 75, 50
    for i in range(24):
        angle = i * (360 / 24)
        rad = np.radians(angle)
        length = 100
        x1 = focus_x + length * np.cos(rad)
        y1 = focus_y + length * np.sin(rad)
        lw = np.random.choice([1.5, 2.0, 3.0, 4.0])
        ax.plot([focus_x, x1], [focus_y, y1], color="black", linewidth=lw)
    ax.plot(focus_x, focus_y, "o", color="black", markersize=15)
    save(fig, "converging_perspective")


if __name__ == "__main__":
    converging_perspective()
