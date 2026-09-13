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


def abstract_parallel_lines_diagonal_stepped_cascade_pattern_black_white_texture():
    """Garis-garis paralel dengan patahan tangga 90 derajat yang bergeser diagonal membentuk kaskade"""
    fig, ax = setup_ax()

    n_lines = 44
    step_height = 8.0
    y_vals = np.linspace(-15, 95, n_lines)

    for i, y0 in enumerate(y_vals):
        # Titik transisi patahan tangga bergeser diagonal melintasi kanvas
        t = i / (n_lines - 1)
        x_step = -5.0 + t * 110.0

        # Segmen 1: horizontal datar kiri
        # Segmen 2: vertikal patahan siku (90 derajat)
        # Segmen 3: horizontal datar kanan
        xs = np.array([-10.0, x_step, x_step, 110.0])
        ys = np.array([y0, y0, y0 + step_height, y0 + step_height])

        # Ritme ketebalan garis berulang
        if i % 3 == 0:
            lw = 3.0
        elif i % 3 == 1:
            lw = 1.8
        else:
            lw = 1.0

        ax.plot(xs, ys, color="black", linewidth=lw, solid_joinstyle="miter")

    save(fig, "abstract_parallel_lines_diagonal_stepped_cascade_pattern_black_white_texture")


if __name__ == "__main__":
    abstract_parallel_lines_diagonal_stepped_cascade_pattern_black_white_texture()
