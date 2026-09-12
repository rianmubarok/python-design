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


def interference_waves():
    fig, ax = setup_ax()
    x = np.linspace(-5, 105, 500)
    y = np.linspace(-5, 105, 500)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X * 0.5) * np.sin(Y * 0.5)
    Z = (Z - Z.min()) / (Z.max() - Z.min())
    n_levels = 30
    levels = np.linspace(0, 1, n_levels)
    ax.contour(X, Y, Z, levels=levels, colors='black', linewidths=0.8)
    save(fig, "interference_waves")


if __name__ == "__main__":
    interference_waves()
