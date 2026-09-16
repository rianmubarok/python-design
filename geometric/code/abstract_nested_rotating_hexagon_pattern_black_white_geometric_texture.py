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


def nested_rotating_hexagon():
    """Wild combo: nested rotating squares x hexagonal tessellation, spun into a rosette"""
    fig, ax = setup_ax()
    cx, cy = 50, 50
    n_hex = 30
    for i in range(n_hex):
        t = i / (n_hex - 1)
        r = 3 + i * 1.7
        ang = np.radians(i * 4.0) + np.arange(7) * (2 * np.pi / 6)
        xs = cx + r * np.cos(ang)
        ys = cy + r * np.sin(ang)
        lw = 1.0 + 2.0 * t
        ax.plot(xs, ys, color="black", linewidth=lw)
    save(fig, "abstract_nested_rotating_hexagon_pattern_black_white_geometric_texture")


if __name__ == "__main__":
    nested_rotating_hexagon()
