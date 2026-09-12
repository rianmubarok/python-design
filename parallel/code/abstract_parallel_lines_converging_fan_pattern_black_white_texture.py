import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

JPG_DIR = Path("output/jpg")
SVG_DIR = Path("output/svg")
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
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
def abstract_parallel_lines_converging_fan_pattern_black_white_texture():
    """Garis paralel yang konvergen membentuk kipas"""
    fig, ax = setup_ax()
    cx, cy = 50, 100
    n_lines = 40
    for i in range(n_lines):
        angle = -70 + i * (140 / n_lines)
        rad = np.radians(angle)
        x1 = cx
        y1 = cy
        x2 = cx + 120 * np.cos(rad)
        y2 = cy + 120 * np.sin(rad)
        lw = 1.5 + 2.0 * np.abs(np.sin(i * 0.3))
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=lw)
    save(fig, "abstract_parallel_lines_converging_fan_pattern_black_white_texture")


if __name__ == "__main__":
    abstract_parallel_lines_converging_fan_pattern_black_white_texture()
