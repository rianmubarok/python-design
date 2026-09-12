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
def checkerboard_wave():
    fig, ax = setup_ax()
    size = 5
    for i, x in enumerate(np.arange(-5, 105, size)):
        for j, y in enumerate(np.arange(-5, 105, size)):
            if (i + j) % 2 == 0:
                cx_sq = x + size / 2
                cy_sq = y + size / 2
                wave_x = 1.5 * np.sin(cy_sq * 0.2)
                wave_y = 1.5 * np.sin(cx_sq * 0.2)
                rect = plt.Rectangle((x + wave_x, y + wave_y), size, size, color="black")
                ax.add_patch(rect)
    save(fig, "checkerboard_wave")


if __name__ == "__main__":
    checkerboard_wave()
