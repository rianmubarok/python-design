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
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name}_{DATE}.jpg"
    svg_path = SVG_DIR / f"{name}_{DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def nested_rotating_squares_drift():
    """Tweak: the nesting center slides toward a corner as the squares grow"""
    fig, ax = setup_ax()
    corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    n_squares = 30
    for i in range(n_squares):
        t = i / (n_squares - 1)
        size = 2 + i * 1.3
        cx = 40 + 18 * t
        cy = 40 + 18 * t
        angle = i * 5.0
        rad = np.radians(angle)
        xs, ys = [], []
        for dx, dy in corners:
            rx = dx * size * np.cos(rad) - dy * size * np.sin(rad)
            ry = dx * size * np.sin(rad) + dy * size * np.cos(rad)
            xs.append(cx + rx)
            ys.append(cy + ry)
        xs.append(xs[0])
        ys.append(ys[0])
        lw = 1.0 + 2.0 * t
        ax.plot(xs, ys, color="black", linewidth=lw)
    save(fig, "abstract_nested_rotating_squares_drift_pattern_black_white_geometric_texture")


if __name__ == "__main__":
    nested_rotating_squares_drift()
