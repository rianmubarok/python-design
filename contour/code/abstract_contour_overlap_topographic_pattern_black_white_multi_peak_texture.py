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
def contour_overlap():
    fig, ax = setup_ax()
    centers = [(30, 30), (70, 30), (50, 70)]
    n_rings = 25
    for cx, cy in centers:
        for i in range(n_rings):
            r = 1 + i * 2.5
            theta = np.linspace(0, 2 * np.pi, 200)
            noise = 1.0 * np.sin(6 * theta + i * 0.4)
            x = cx + (r + noise) * np.cos(theta)
            y = cy + (r + noise) * np.sin(theta)
            lw = 0.8 + 1.0 * (1 - i / n_rings)
            ax.plot(x, y, color="black", linewidth=lw)
    save(fig, "contour_overlap")


if __name__ == "__main__":
    contour_overlap()
