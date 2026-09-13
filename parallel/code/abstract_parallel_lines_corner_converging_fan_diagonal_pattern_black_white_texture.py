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


def abstract_parallel_lines_corner_converging_fan_diagonal_pattern_black_white_texture():
    """Garis kipas konvergen memancar dari sudut kiri-bawah secara diagonal melintasi kanvas"""
    fig, ax = setup_ax()

    x0, y0 = -5.0, -5.0
    n_rays = 60
    length = 160.0

    angles = np.linspace(2.0, 88.0, n_rays)

    for i, deg in enumerate(angles):
        rad = np.radians(deg)
        x1 = x0 + length * np.cos(rad)
        y1 = y0 + length * np.sin(rad)

        # Gradasi ketebalan garis dengan aksentuasi di poros diagonal 45 derajat
        center_dist = abs(deg - 45.0) / 45.0
        lw = 1.0 + 2.5 * (1.0 - center_dist ** 1.5)

        ax.plot([x0, x1], [y0, y1], color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract_parallel_lines_corner_converging_fan_diagonal_pattern_black_white_texture")


if __name__ == "__main__":
    abstract_parallel_lines_corner_converging_fan_diagonal_pattern_black_white_texture()
