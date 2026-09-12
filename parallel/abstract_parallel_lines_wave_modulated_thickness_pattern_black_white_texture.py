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


def parallel_wave_modulated():
    """Garis paralel dengan ketebalan modulasi gelombang"""
    fig, ax = setup_ax()

    n_lines = 50
    x = np.linspace(-5, 105, 100)
    for i in range(n_lines):
        y = -5 + i * 2.2
        wave = np.sin(x * 0.12 + i * 0.5)
        segments = np.array([[x[j], y, x[j+1], y] for j in range(len(x)-1)])
        from matplotlib.collections import LineCollection
        lc = LineCollection(segments.reshape(-1, 2, 2), linewidths=1.5 + wave[:-1] * 1.0, color='black')
        ax.add_collection(lc)

    save(fig, "parallel_wave_modulated")


if __name__ == "__main__":
    parallel_wave_modulated()
