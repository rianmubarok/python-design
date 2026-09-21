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


def abstract_parallel_lines_running_bond_staggered_dash_pattern_black_white_texture():
    """Garis strip paralel tersusun selang-seling 50 persen (running bond masonry) dengan jarak vertikal membesar"""
    fig, ax = setup_ax()

    dash_len = 9.0
    gap_len = 1.8
    stride = dash_len + gap_len

    # Jarak baris vertikal membesar dari atas ke bawah (skala vertikal progresif)
    y_levels = []
    curr_y = 104.0
    dy = 1.2
    factor = 1.045
    while curr_y > -4.0:
        y_levels.append(curr_y)
        curr_y -= dy
        dy *= factor

    for row_idx, y in enumerate(y_levels):
        # Pola selang-seling 50%
        offset = (stride / 2.0) if (row_idx % 2 == 1) else 0.0

        # Ketebalan garis proporsional dengan jarak baris
        progress = row_idx / len(y_levels)
        lw = 1.0 + 2.8 * (progress ** 1.3)

        curr_x = -15.0 + offset
        while curr_x < 115.0:
            x_end = curr_x + dash_len
            ax.plot([curr_x, x_end], [y, y], color="black", linewidth=lw, solid_capstyle="butt")
            curr_x = x_end + gap_len

    save(fig, "abstract parallel lines running bond staggered dash pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_running_bond_staggered_dash_pattern_black_white_texture()
