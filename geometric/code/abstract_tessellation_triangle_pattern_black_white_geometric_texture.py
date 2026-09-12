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
def tessellation():
    fig, ax = setup_ax()
    size = 8
    h = size * np.sqrt(3) / 2
    for row in range(-1, 15):
        for col in range(-1, 15):
            x = col * size + (row % 2) * size / 2
            y = row * h
            if (row + col) % 2 == 0:
                triangle = [(x, y), (x + size, y), (x + size / 2, y + h)]
            else:
                triangle = [(x, y + h), (x + size, y + h), (x + size / 2, y)]
            xs = [p[0] for p in triangle] + [triangle[0][0]]
            ys = [p[1] for p in triangle] + [triangle[0][1]]
            ax.plot(xs, ys, color="black", linewidth=0.8)
    save(fig, "tessellation")


if __name__ == "__main__":
    tessellation()
