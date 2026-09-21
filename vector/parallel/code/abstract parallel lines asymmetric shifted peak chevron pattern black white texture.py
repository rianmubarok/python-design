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


def abstract_parallel_lines_asymmetric_shifted_peak_chevron_pattern_black_white_texture():
    """Garis chevron paralel dengan posisi puncak tergeser asimetris ke 72 persen lebar kanvas"""
    fig, ax = setup_ax()

    n_lines = 48
    peak_x = 72.0
    lift = 28.0

    y_base = np.linspace(-30, 110, n_lines)

    for i, y0 in enumerate(y_base):
        # Titik sudut: kiri (-10), puncak asimetris (peak_x), kanan (110)
        xs = np.array([-10.0, peak_x, 110.0])
        ys = np.array([y0, y0 + lift, y0])

        # Ritme ketebalan garis berselang-seling
        if i % 4 == 0:
            lw = 3.2
        elif i % 2 == 0:
            lw = 2.0
        else:
            lw = 1.0

        ax.plot(xs, ys, color="black", linewidth=lw, solid_joinstyle="miter")

    save(fig, "abstract parallel lines asymmetric shifted peak chevron pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_asymmetric_shifted_peak_chevron_pattern_black_white_texture()
