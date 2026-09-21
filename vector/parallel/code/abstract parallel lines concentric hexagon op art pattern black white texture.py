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


def abstract_parallel_lines_concentric_hexagon_op_art_pattern_black_white_texture():
    """Cincin garis heksagonal konsentris bersarang dengan modulasi ketebalan berirama gaya op-art"""
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_hexagons = 34
    max_r = 75.0
    radii = np.linspace(4.0, max_r, n_hexagons)

    angles = np.radians(np.array([0, 60, 120, 180, 240, 300, 360]))

    for i, r in enumerate(radii):
        hx = cx + r * np.cos(angles)
        hy = cy + r * np.sin(angles)

        # Ritme ketebalan garis op-art 3-cadence
        if i % 3 == 0:
            lw = 3.4
        elif i % 3 == 1:
            lw = 1.0
        else:
            lw = 2.0

        ax.plot(hx, hy, color="black", linewidth=lw, solid_joinstyle="miter")

    save(fig, "abstract parallel lines concentric hexagon op art pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_concentric_hexagon_op_art_pattern_black_white_texture()
