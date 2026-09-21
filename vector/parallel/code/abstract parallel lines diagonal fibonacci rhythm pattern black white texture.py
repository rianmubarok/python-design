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


def abstract_parallel_lines_diagonal_fibonacci_rhythm_pattern_black_white_texture():
    """Garis paralel diagonal 45 derajat dengan ritme jarak dan ketebalan berskala Fibonacci progresif"""
    fig, ax = setup_ax()

    # Sumbu tegak lurus diagonal 45 derajat berjarak dari -80 sampai 180
    # Rasio pertambahan jarak dan ketebalan teratur
    offsets = []
    curr = -60.0
    step = 1.2
    factor = 1.055

    while curr < 200.0:
        offsets.append(curr)
        curr += step
        step *= factor

    # Buat garis 45 derajat (y - x = c) -> y = x + c
    for i, c in enumerate(offsets):
        x_vals = np.array([-20.0, 120.0])
        y_vals = x_vals + c

        # Ketebalan garis proporsional dengan skala ruang
        progress = i / len(offsets)
        lw = 0.8 + 3.6 * (progress ** 1.5)

        ax.plot(x_vals, y_vals, color="black", linewidth=lw, solid_capstyle="butt")

    save(fig, "abstract parallel lines diagonal fibonacci rhythm pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_diagonal_fibonacci_rhythm_pattern_black_white_texture()
