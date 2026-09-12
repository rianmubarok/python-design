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


def labyrinth():
    fig, ax = setup_ax()
    cell_size = 5
    rows = 20
    cols = 20
    np.random.seed(SEED)
    for r in range(rows):
        for c in range(cols):
            x = c * cell_size
            y = r * cell_size
            if np.random.random() > 0.5:
                ax.plot([x, x + cell_size], [y, y], color="black", linewidth=1.2)
            if np.random.random() > 0.5:
                ax.plot([x, x], [y, y + cell_size], color="black", linewidth=1.2)
            if np.random.random() > 0.3:
                ax.plot([x + cell_size, x + cell_size], [y, y + cell_size], color="black", linewidth=1.2)
            if np.random.random() > 0.3:
                ax.plot([x, x + cell_size], [y + cell_size, y + cell_size], color="black", linewidth=1.2)
    save(fig, "labyrinth")


if __name__ == "__main__":
    labyrinth()
