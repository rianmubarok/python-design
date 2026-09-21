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


def abstract_parallel_lines_frequency_sweep_chirp_pattern_black_white_texture():
    """Garis paralel sinus dengan akselerasi frekuensi spasial (chirp wave) dari kiri ke kanan"""
    fig, ax = setup_ax()

    n_lines = 46
    y_vals = np.linspace(-5, 105, n_lines)
    x = np.linspace(-5, 105, 600)
    x_norm = (x - (-5)) / 110.0  # 0 ke 1

    # Frekuensi chirp bertambah dari f0=1.0 ke f1=10.0
    f0, f1 = 1.0, 10.0
    chirp_phase = 2 * np.pi * (f0 * x_norm + 0.5 * (f1 - f0) * (x_norm ** 2.2))

    for i, y0 in enumerate(y_vals):
        amplitude = 3.5
        y = y0 + amplitude * np.sin(chirp_phase)

        # Gradasi ketebalan garis dari atas ke bawah
        progress = i / (n_lines - 1)
        lw = 1.0 + 2.4 * progress

        ax.plot(x, y, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines frequency sweep chirp pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_frequency_sweep_chirp_pattern_black_white_texture()
