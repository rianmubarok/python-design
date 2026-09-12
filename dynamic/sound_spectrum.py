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


def sound_spectrum():
    fig, ax = setup_ax()
    n_bars = 80
    x_positions = np.linspace(-5, 105, n_bars)
    for i, x in enumerate(x_positions):
        height = 30 + 40 * np.sin(i * 0.3) * np.cos(i * 0.15)
        height = max(10, min(height, 90))
        y_base = 50 - height / 2
        y_top = 50 + height / 2
        lw = 1.0 + 0.8 * np.sin(i * 0.2)
        ax.plot([x, x], [y_base, y_top], color="black", linewidth=lw)
    save(fig, "sound_spectrum")


if __name__ == "__main__":
    sound_spectrum()
