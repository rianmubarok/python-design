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
def mandala():
    fig, ax = setup_ax()
    cx, cy = 50, 50
    n_petals = 12
    n_rings = 8
    for ring in range(n_rings):
        r = 5 + ring * 6
        theta = np.linspace(0, 2 * np.pi, 200)
        x = cx + r * np.cos(theta)
        y = cy + r * np.sin(theta)
        lw = 1.0 + 1.5 * (ring / n_rings)
        ax.plot(x, y, color="black", linewidth=lw)
    for i in range(n_petals):
        angle = i * (360 / n_petals)
        for j in range(1, n_rings + 1):
            r = 5 + j * 6
            petal_angle = np.linspace(-15, 15, 30) + angle
            rad = np.radians(petal_angle)
            x = cx + r * np.cos(rad)
            y = cy + r * np.sin(rad)
            lw = 0.8 + 1.0 * (j / n_rings)
            ax.plot(x, y, color="black", linewidth=lw)
    ax.plot(cx, cy, "o", color="black", markersize=10)
    save(fig, "mandala")


if __name__ == "__main__":
    mandala()
