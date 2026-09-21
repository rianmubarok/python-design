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


def abstract_parallel_lines_vortex_swirl_distortion_pattern_black_white_texture():
    """Wild: straight rasters caught in a fluid vortex, rotation decays with radius"""
    fig, ax = setup_ax()
    cx, cy = 50.0, 50.0
    strength = 2.3
    sigma = 30.0
    n_lines = 64
    x = np.linspace(-5, 105, 800)

    for i in range(n_lines):
        y0 = -5 + i * (110 / (n_lines - 1))
        y = np.full_like(x, y0)
        dx = x - cx
        dy = y - cy
        r = np.hypot(dx, dy)
        ang = strength * np.exp(-((r / sigma) ** 2))
        xr = cx + dx * np.cos(ang) - dy * np.sin(ang)
        yr = cy + dx * np.sin(ang) + dy * np.cos(ang)
        lw = 0.6 + 1.9 * np.exp(-((abs(y0 - cy) / sigma) ** 2))
        ax.plot(xr, yr, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines vortex swirl distortion pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_vortex_swirl_distortion_pattern_black_white_texture()
