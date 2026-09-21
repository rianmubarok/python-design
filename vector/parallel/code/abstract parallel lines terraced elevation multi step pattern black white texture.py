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


def abstract_parallel_lines_terraced_elevation_multi_step_pattern_black_white_texture():
    """Garis paralel multi-undakan bertingkat (3 level elevasi) menyerupai kontur arsitektural"""
    fig, ax = setup_ax()

    n_lines = 40
    y_vals = np.linspace(-18, 90, n_lines)

    x_step1 = 28.0
    x_step2 = 54.0
    x_step3 = 80.0
    lift1 = 4.5
    lift2 = 9.0
    lift3 = 13.5

    for i, y0 in enumerate(y_vals):
        # Profil 4 plato datar dan 3 tanjakan vertikal
        xs = np.array([
            -10.0, x_step1, x_step1,
            x_step2, x_step2,
            x_step3, x_step3,
            110.0
        ])
        ys = np.array([
            y0, y0, y0 + lift1,
            y0 + lift1, y0 + lift2,
            y0 + lift2, y0 + lift3,
            y0 + lift3
        ])

        lw = 1.0 + 2.2 * np.abs(np.sin(i * 0.28))
        ax.plot(xs, ys, color="black", linewidth=lw, solid_joinstyle="miter")

    save(fig, "abstract parallel lines terraced elevation multi step pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_terraced_elevation_multi_step_pattern_black_white_texture()
