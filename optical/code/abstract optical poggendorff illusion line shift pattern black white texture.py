import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
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
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
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


def abstract_optical_poggendorff_illusion_line_shift_pattern_black_white_texture():
    """Poggendorff Illusion pattern with visible vertical masking bars and line shift effect."""
    fig, ax = setup_ax()

    bar_left = 38
    bar_right = 62
    n_lines = 35
    y_starts = np.linspace(-30, 100, n_lines)

    # Offset vertikal untuk menciptakan/memperkuat ilusi pergeseran garis Poggendorff
    shift_offset = 2.5

    for y0 in y_starts:
        # Garis diagonal sisi kiri (berhenti di batas kiri batang)
        y_left_end = y0 + bar_left
        ax.plot([0, bar_left], [y0, y_left_end], color="black", linewidth=1.5, zorder=1)

        # Garis diagonal sisi kanan (mulai dari batas kanan batang dengan offset)
        y_right_start = y0 + bar_right + shift_offset
        y_right_end = y0 + 100 + shift_offset
        ax.plot([bar_right, 100], [y_right_start, y_right_end], color="black", linewidth=1.5, zorder=1)

    # Batang penghalang vertikal di tengah
    bar = Rectangle((bar_left, 0), bar_right - bar_left, 100, fill=True, facecolor="black", zorder=2)
    ax.add_patch(bar)

    # Garis tepi putih/kontras untuk memperjelas struktur isolasi
    ax.plot([bar_left, bar_left], [0, 100], color="white", linewidth=1.0, zorder=3)
    ax.plot([bar_right, bar_right], [0, 100], color="white", linewidth=1.0, zorder=3)

    save(fig, "abstract optical poggendorff illusion line shift pattern black white texture")


if __name__ == "__main__":
    abstract_optical_poggendorff_illusion_line_shift_pattern_black_white_texture()