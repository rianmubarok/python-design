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
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def abstract_parallel_lines_moire_interference_rotation_pattern_black_white_texture():
    """Wild: two identical line rasters rotated apart so beating creates moire bands"""
    fig, ax = setup_ax()
    cx, cy = 50.0, 50.0
    n_lines = 160
    angle = np.deg2rad(4.0)
    ca, sa = np.cos(angle), np.sin(angle)

    for i in range(n_lines):
        x = -5 + i * (110 / (n_lines - 1))
        ax.plot([x, x], [-5, 105], color="black", linewidth=0.5)

    for i in range(n_lines):
        x = -5 + i * (110 / (n_lines - 1))
        p1 = (cx + (x - cx) * ca - (-5 - cy) * sa, cy + (x - cx) * sa + (-5 - cy) * ca)
        p2 = (cx + (x - cx) * ca - (105 - cy) * sa, cy + (x - cx) * sa + (105 - cy) * ca)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="black", linewidth=0.5)

    save(fig, "abstract parallel lines moire interference rotation pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_moire_interference_rotation_pattern_black_white_texture()
