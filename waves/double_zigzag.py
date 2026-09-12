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


def double_zigzag():
    fig, ax = setup_ax()
    n_pairs = 8
    for i in range(n_pairs):
        y_base = -5 + i * 13
        amp = np.random.uniform(4, 7)
        freq = np.random.randint(5, 9)
        phase = np.random.uniform(0, np.pi)
        lw = np.random.choice([1.5, 2.0, 2.5])
        x = np.linspace(-5, 105, 300)
        y1 = y_base + amp * np.sin(freq * x * np.pi / 100 + phase)
        y2 = y_base + amp * np.sin(freq * x * np.pi / 100 + phase + np.pi)
        ax.plot(x, y1, color="black", linewidth=lw)
        ax.plot(x, y2, color="black", linewidth=lw)
    save(fig, "double_zigzag")


if __name__ == "__main__":
    double_zigzag()
