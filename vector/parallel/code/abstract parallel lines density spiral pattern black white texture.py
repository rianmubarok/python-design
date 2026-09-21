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


def abstract_parallel_lines_density_spiral_pattern_black_white_texture():
    fig, ax = setup_ax()
    n_lines = 30
    center_x, center_y = 50, 50
    for i in range(n_lines):
        y = -5 + i * (110 / n_lines)
        dist = np.sqrt((y - center_y) ** 2)
        max_dist = 55
        density_factor = 1 - dist / max_dist
        n_segments = int(5 + 15 * density_factor)
        segment_length = 110 / n_segments
        for j in range(n_segments):
            x_start = -5 + j * segment_length
            x_end = x_start + segment_length * 0.6
            ax.plot([x_start, x_end], [y, y], color="black", linewidth=0.5 + 1.5 * density_factor)
    save(fig, "abstract parallel lines density spiral pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_density_spiral_pattern_black_white_texture()
