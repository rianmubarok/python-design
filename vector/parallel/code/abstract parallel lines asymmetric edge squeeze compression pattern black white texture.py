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


def abstract_parallel_lines_asymmetric_edge_squeeze_compression_pattern_black_white_texture():
    """Garis-garis paralel vertikal dengan kompresi sangat padat di margin kiri dan meregang ke kanan"""
    fig, ax = setup_ax()

    # Hitung posisi x vertikal dengan fungsi eksponensial (padat di kiri, renggang di kanan)
    x_positions = []
    curr_x = -5.0
    dx = 0.45
    growth_rate = 1.052

    while curr_x < 106.0:
        x_positions.append(curr_x)
        curr_x += dx
        dx *= growth_rate

    n_lines = len(x_positions)
    for i, x in enumerate(x_positions):
        progress = i / (n_lines - 1)
        # Ketebalan membesar sebanding dengan kelonggaran ruang
        lw = 0.6 + 3.4 * (progress ** 1.4)
        ax.plot([x, x], [-5.0, 105.0], color="black", linewidth=lw, solid_capstyle="butt")

    save(fig, "abstract parallel lines asymmetric edge squeeze compression pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_asymmetric_edge_squeeze_compression_pattern_black_white_texture()
