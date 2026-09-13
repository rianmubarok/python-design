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


def abstract_parallel_lines_droplet_ripple_distortion_pattern_black_white_texture():
    """Garis paralel lurus horizontal yang terdistorsi riak tetesan air di posisi asimetris"""
    fig, ax = setup_ax()

    cx, cy = 38.0, 62.0
    amplitude = 12.0
    wavelength = 8.5
    decay_sigma = 28.0

    n_lines = 58
    y_base = np.linspace(-5, 105, n_lines)
    x = np.linspace(-5, 105, 500)

    for i, y0 in enumerate(y_base):
        # Hitung jarak dari tiap titik pada garis ke titik pusat riak (cx, cy)
        r = np.hypot(x - cx, y0 - cy)
        decay = np.exp(-((r / decay_sigma) ** 2))
        wave = amplitude * np.sin(2 * np.pi * r / wavelength) * decay

        y = y0 + wave
        # Modulasi ketebalan garis secara halus per garis berdasarkan kedekatan dengan pusat riak
        line_dist = abs(y0 - cy)
        line_decay = np.exp(-((line_dist / decay_sigma) ** 2))
        lw = 1.0 + 2.4 * line_decay

        ax.plot(x, y, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract_parallel_lines_droplet_ripple_distortion_pattern_black_white_texture")


if __name__ == "__main__":
    abstract_parallel_lines_droplet_ripple_distortion_pattern_black_white_texture()
