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


def abstract_parallel_lines_gradient_dash_stride_scale_pattern_black_white_texture():
    """Garis putus-putus paralel dengan panjang segmen membesar dari titik mikro di kiri ke balok makro di kanan"""
    fig, ax = setup_ax()

    n_lines = 50
    y_vals = np.linspace(-5, 105, n_lines)

    for i, y in enumerate(y_vals):
        curr_x = -5.0
        row_offset = (i % 2) * 1.5
        curr_x += row_offset

        lw = 1.4 + 1.2 * (i % 3 == 0)

        while curr_x < 105.0:
            # Proporsi posisi x saat ini (0 sampai 1)
            t = np.clip((curr_x - (-5.0)) / 110.0, 0.0, 1.0)
            # Panjang dash membesar progresif: dari 0.8 (mikro) hingga 12.0 (makro)
            dash_len = 0.8 + 11.2 * (t ** 1.8)
            gap_len = 2.0

            x_end = min(curr_x + dash_len, 105.0)
            ax.plot([curr_x, x_end], [y, y], color="black", linewidth=lw, solid_capstyle="butt")
            curr_x = x_end + gap_len

    save(fig, "abstract parallel lines gradient dash stride scale pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_gradient_dash_stride_scale_pattern_black_white_texture()
