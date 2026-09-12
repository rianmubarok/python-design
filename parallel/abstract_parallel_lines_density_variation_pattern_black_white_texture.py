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


def parallel_density():
    fig, ax = setup_ax()
    y = -5
    while y < 105:
        dist_from_center = abs(y - 50) / 50
        density = 0.5 + 2.0 * (1 - dist_from_center)
        n_segments = int(density * 15)
        x_segments = np.linspace(-5, 105, n_segments + 1)
        for j in range(n_segments):
            x1 = x_segments[j]
            x2 = x_segments[j + 1]
            lw = 1.0 + 2.0 * (1 - dist_from_center)
            ax.plot([x1, x2], [y, y], color="black", linewidth=lw)
        y += 1.5 + 1.5 * dist_from_center
    save(fig, "parallel_density")


if __name__ == "__main__":
    parallel_density()
