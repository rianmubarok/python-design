import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def abstract_grid_tessellation_hilbert_curve_maze_pattern_black_white_texture():
    """Generates a space-filling Hilbert curve which creates a continuous maze-like grid pattern."""
    fig, ax = setup_ax()

    def hilbert(x0, y0, xi, xj, yi, yj, n, lines):
        if n <= 0:
            X = x0 + (xi + yi) / 2
            Y = y0 + (xj + yj) / 2
            lines.append((X, Y))
        else:
            hilbert(x0,               y0,               yi/2, yj/2, xi/2, xj/2, n - 1, lines)
            hilbert(x0 + xi/2,        y0 + xj/2,        xi/2, xj/2, yi/2, yj/2, n - 1, lines)
            hilbert(x0 + xi/2 + yi/2, y0 + xj/2 + yj/2, xi/2, xj/2, yi/2, yj/2, n - 1, lines)
            hilbert(x0 + xi/2 + yi,   y0 + xj/2 + yj,  -yi/2,-yj/2,-xi/2,-xj/2, n - 1, lines)

    lines = []
    # Generate 6th order Hilbert curve (dense grid)
    hilbert(0.0, 0.0, 100.0, 0.0, 0.0, 100.0, 6, lines)
    
    x_vals = [p[0] for p in lines]
    y_vals = [p[1] for p in lines]
    
    # Plot the continuous space-filling line
    ax.plot(x_vals, y_vals, color="black", linewidth=2.0, solid_joinstyle='miter')
    
    # Also add a slightly thicker white line underneath to create a 'trench' effect if we add offset
    # ax.plot(np.array(x_vals)+0.5, np.array(y_vals)-0.5, color="white", linewidth=3.0, zorder=1)

    save(fig, "abstract grid tessellation hilbert curve maze pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_hilbert_curve_maze_pattern_black_white_texture()
