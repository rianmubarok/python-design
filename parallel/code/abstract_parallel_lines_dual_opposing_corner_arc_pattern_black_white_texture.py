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


def abstract_parallel_lines_dual_opposing_corner_arc_pattern_black_white_texture():
    """Garis paralel busur dari dua sudut berseberangan yang bertemu di garis diagonal"""
    fig, ax = setup_ax()

    n_arcs = 36
    max_r = 110
    radii = np.linspace(8, max_r, n_arcs)
    theta1 = np.linspace(0, np.pi / 2, 350)
    theta2 = np.linspace(np.pi, 3 * np.pi / 2, 350)

    # Busur dari sudut kiri-bawah (-5, -5)
    for i, r in enumerate(radii):
        x = -5 + r * np.cos(theta1)
        y = -5 + r * np.sin(theta1)
        lw = 1.0 + 1.8 * ((n_arcs - i) / n_arcs)
        ax.plot(x, y, color="black", linewidth=lw, solid_capstyle="round")

    # Busur dari sudut kanan-atas (105, 105)
    for i, r in enumerate(radii):
        x = 105 + r * np.cos(theta2)
        y = 105 + r * np.sin(theta2)
        lw = 1.0 + 1.8 * (i / n_arcs)
        ax.plot(x, y, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract_parallel_lines_dual_opposing_corner_arc_pattern_black_white_texture")


if __name__ == "__main__":
    abstract_parallel_lines_dual_opposing_corner_arc_pattern_black_white_texture()
