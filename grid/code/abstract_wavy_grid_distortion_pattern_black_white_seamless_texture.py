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
def wavy_grid():
    fig, ax = setup_ax()
    n_lines = 20
    for i in range(n_lines):
        y_base = -5 + i * 5.5
        x = np.linspace(-5, 105, 300)
        amp = 2 * np.sin(i * 0.5)
        y = y_base + amp * np.sin(x * 0.1 + i * 0.3)
        ax.plot(x, y, color="black", linewidth=0.8)
    for i in range(n_lines):
        x_base = -5 + i * 5.5
        y = np.linspace(-5, 105, 300)
        amp = 2 * np.cos(i * 0.5)
        x = x_base + amp * np.sin(y * 0.1 + i * 0.3)
        ax.plot(x, y, color="black", linewidth=0.8)
    save(fig, "wavy_grid")


if __name__ == "__main__":
    wavy_grid()
