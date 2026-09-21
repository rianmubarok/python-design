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


def abstract_parallel_lines_zigzag_amplitude_gradient_scale_pattern_black_white_texture():
    """Garis paralel zigzag dengan amplitudo membesar progresif dari mikro di atas ke makro di bawah"""
    fig, ax = setup_ax()

    n_lines = 44
    n_peaks = 12
    # Titik x untuk zigzag (puncak dan lembah)
    x_pts = np.linspace(-10, 110, n_peaks * 2 + 1)
    # Tanda selang-seling (+1 untuk puncak, -1 untuk lembah)
    signs = np.array([1 if i % 2 == 1 else -1 for i in range(len(x_pts))])
    signs[0] = 0
    signs[-1] = 0

    y_vals = np.linspace(102, -2, n_lines)  # dari atas ke bawah

    for i, y_base in enumerate(y_vals):
        progress = i / (n_lines - 1)  # 0 di atas, 1 di bawah
        amplitude = 0.4 + 6.2 * (progress ** 1.6)
        y_pts = y_base + signs * amplitude

        lw = 0.8 + 2.4 * (progress ** 1.2)
        ax.plot(x_pts, y_pts, color="black", linewidth=lw, solid_joinstyle="miter")

    save(fig, "abstract parallel lines zigzag amplitude gradient scale pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_zigzag_amplitude_gradient_scale_pattern_black_white_texture()
