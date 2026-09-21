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


def abstract_parallel_lines_diagonal_split_herringbone_mirror_pattern_black_white_texture():
    """Garis paralel diagonal terbelah simetris di garis tengah (chevron/herringbone mirror)"""
    fig, ax = setup_ax()

    mid_x = 50.0
    n_lines = 52
    spacing = 150.0 / n_lines

    for i in range(-15, n_lines + 20):
        y_intercept = -20.0 + i * spacing

        # Sisi Kiri (x: -10 sampai 50, kemiringan +45 derajat)
        x_left = np.array([-10.0, mid_x])
        y_left = y_intercept + (x_left - (-10.0))

        # Sisi Kanan (x: 50 sampai 110, kemiringan -45 derajat)
        x_right = np.array([mid_x, 110.0])
        y_right = (y_intercept + (mid_x - (-10.0))) - (x_right - mid_x)

        # Pola ketebalan berirama dinamis
        lw = 1.2 + 2.4 * np.abs(np.sin(i * 0.22))

        ax.plot(x_left, y_left, color="black", linewidth=lw, solid_capstyle="butt")
        ax.plot(x_right, y_right, color="black", linewidth=lw, solid_capstyle="butt")

    save(fig, "abstract parallel lines diagonal split herringbone mirror pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_diagonal_split_herringbone_mirror_pattern_black_white_texture()
