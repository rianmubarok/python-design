import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

SIZE = 4000
DPI = 300
SEED = 42

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
    png_path = PNG_DIR / f"{name}.png"
    svg_path = SVG_DIR / f"{name}.svg"
    fig.savefig(png_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {png_path} | {svg_path}")


def radial_sunburst():
    fig, ax = setup_ax()
    cx, cy = 20, 50
    n_lines = 35
    for i in range(n_lines):
        angle = -80 + i * (160 / n_lines)
        rad = np.radians(angle)
        length = 100
        x2 = cx + length * np.cos(rad)
        y2 = cy + length * np.sin(rad)
        lw = np.random.choice([1.5, 2.0, 3.0, 4.0, 5.0])
        ax.plot([cx, x2], [cy, y2], color="black", linewidth=lw)
    ax.plot(cx, cy, "o", color="black", markersize=15)
    save(fig, "radial_sunburst")


if __name__ == "__main__":
    radial_sunburst()
