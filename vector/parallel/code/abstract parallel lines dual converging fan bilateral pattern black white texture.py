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


def abstract_parallel_lines_dual_converging_fan_bilateral_pattern_black_white_texture():
    """Dua kipas konvergen bilateral dari tepi kiri dan kanan yang saling bersilangan harmonis"""
    fig, ax = setup_ax()

    n_rays = 44
    angles = np.linspace(-48.0, 48.0, n_rays)
    length = 130.0

    # Kipas sisi kiri (x=-10, y=50) memancar ke kanan
    x_left, y_left = -10.0, 50.0
    for deg in angles:
        rad = np.radians(deg)
        x1 = x_left + length * np.cos(rad)
        y1 = y_left + length * np.sin(rad)
        lw = 1.0 + 1.2 * np.cos(rad) ** 2
        ax.plot([x_left, x1], [y_left, y1], color="black", linewidth=lw)

    # Kipas sisi kanan (x=110, y=50) memancar ke kiri
    x_right, y_right = 110.0, 50.0
    for deg in angles:
        rad = np.radians(180.0 - deg)
        x1 = x_right + length * np.cos(rad)
        y1 = y_right + length * np.sin(rad)
        lw = 1.0 + 1.2 * np.cos(rad) ** 2
        ax.plot([x_right, x1], [y_right, y1], color="black", linewidth=lw)

    save(fig, "abstract parallel lines dual converging fan bilateral pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_dual_converging_fan_bilateral_pattern_black_white_texture()
