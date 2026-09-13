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


def abstract_parallel_lines_dual_opposing_sine_ribbon_pattern_black_white_texture():
    """Garis paralel dengan modulasi dua gelombang fase berlawanan membentuk pita menjepit dan mengembang"""
    fig, ax = setup_ax()

    n_lines = 50
    y_vals = np.linspace(-5, 105, n_lines)
    x = np.linspace(-5, 105, 500)

    for i, y0 in enumerate(y_vals):
        # Modulasi vertikal berdasarkan posisi y0 terhadap sumbu tengah (50)
        norm_y = (y0 - 50.0) / 55.0  # -1 sampai 1
        # Amplitudo berlawanan arah di atas dan bawah sumbu tengah
        amp = 14.0 * np.sin(norm_y * np.pi * 0.9)
        wave = amp * np.sin(x * np.pi * 4 / 110.0)

        y = y0 + wave
        lw = 1.2 + 2.0 * (np.cos(norm_y * np.pi * 0.5) ** 2)

        ax.plot(x, y, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract_parallel_lines_dual_opposing_sine_ribbon_pattern_black_white_texture")


if __name__ == "__main__":
    abstract_parallel_lines_dual_opposing_sine_ribbon_pattern_black_white_texture()
