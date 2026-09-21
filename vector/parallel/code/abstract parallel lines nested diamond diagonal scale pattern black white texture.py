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


def abstract_parallel_lines_nested_diamond_diagonal_scale_pattern_black_white_texture():
    """Garis paralel belah ketupat (diamond) bersarang 45 derajat dengan ritme ketebalan op-art"""
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_diamonds = 36
    max_d = 75.0

    for i in range(n_diamonds):
        d = 3.5 + i * (max_d / n_diamonds)
        # Koordinat belah ketupat (diamond)
        diamond_x = [cx, cx + d, cx, cx - d, cx]
        diamond_y = [cy + d, cy, cy - d, cy, cy + d]

        # Pola ketebalan berirama (rhythmic alternating cadence)
        if i % 3 == 0:
            lw = 3.2
        elif i % 3 == 1:
            lw = 1.2
        else:
            lw = 2.0

        ax.plot(diamond_x, diamond_y, color="black", linewidth=lw, solid_joinstyle="miter")

    save(fig, "abstract parallel lines nested diamond diagonal scale pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_nested_diamond_diagonal_scale_pattern_black_white_texture()
