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


def abstract_parallel_lines_circular_negative_space_cutout_pattern_black_white_texture():
    """Garis-garis paralel horizontal dengan siluet ruang negatif lingkaran di posisi asimetris"""
    fig, ax = setup_ax()

    # Lingkaran ruang negatif di posisi golden ratio asimetris
    cx, cy = 62.0, 46.0
    radius = 28.0

    n_lines = 64
    y_vals = np.linspace(-5, 105, n_lines)

    for i, y in enumerate(y_vals):
        lw = 1.4 + 1.2 * np.sin(i * 0.18) ** 2

        # Cek apakah garis ini memotong lingkaran ruang negatif
        dist_y = abs(y - cy)
        if dist_y < radius:
            # Setengah lebar potongan lingkaran pada ketinggian y
            dx = np.sqrt(radius ** 2 - dist_y ** 2)
            # Segmen kiri
            ax.plot([-5.0, cx - dx], [y, y], color="black", linewidth=lw, solid_capstyle="round")
            # Segmen kanan
            ax.plot([cx + dx, 105.0], [y, y], color="black", linewidth=lw, solid_capstyle="round")
        else:
            # Garis utuh penuh
            ax.plot([-5.0, 105.0], [y, y], color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract_parallel_lines_circular_negative_space_cutout_pattern_black_white_texture")


if __name__ == "__main__":
    abstract_parallel_lines_circular_negative_space_cutout_pattern_black_white_texture()
