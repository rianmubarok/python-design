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


def abstract_parallel_lines_moire_interference_two_circle_grids_pattern_black_white_texture():
    """Op-art Moiré: two sets of concentric circles offset from each other create interference fringes"""
    fig, ax = setup_ax()

    # Two circle centres slightly offset from canvas centre
    c1 = (47.0, 50.0)
    c2 = (53.0, 50.0)
    n_rings = 68
    max_r = 85.0
    radii = np.linspace(1.5, max_r, n_rings)
    n_pts = 720

    theta = np.linspace(0, 2 * np.pi, n_pts)

    for r in radii:
        # First circle set
        x1 = c1[0] + r * np.cos(theta)
        y1 = c1[1] + r * np.sin(theta)
        lw = 0.28 + 0.55 * (r / max_r) ** 0.5
        ax.plot(x1, y1, color="black", linewidth=lw, solid_capstyle="round")

        # Second circle set
        x2 = c2[0] + r * np.cos(theta)
        y2 = c2[1] + r * np.sin(theta)
        ax.plot(x2, y2, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines moire interference two circle grids pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_moire_interference_two_circle_grids_pattern_black_white_texture()
