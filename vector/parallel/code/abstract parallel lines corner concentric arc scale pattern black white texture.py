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


def abstract_parallel_lines_corner_concentric_arc_scale_pattern_black_white_texture():
    """Garis paralel busur konsentris memancar dari sudut dengan gradasi skala ketebalan"""
    fig, ax = setup_ax()
    cx, cy = -5, -5
    n_arcs = 48
    max_r = 160
    radii = np.linspace(6, max_r, n_arcs)
    theta = np.linspace(0, np.pi / 2, 400)

    for i, r in enumerate(radii):
        x = cx + r * np.cos(theta)
        y = cy + r * np.sin(theta)
        # Variasi ketebalan berirama dengan gradasi progresif
        progress = i / (n_arcs - 1)
        lw = 0.8 + 2.8 * (progress ** 1.3) + 0.6 * np.sin(progress * np.pi * 4) ** 2
        ax.plot(x, y, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines corner concentric arc scale pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_corner_concentric_arc_scale_pattern_black_white_texture()
