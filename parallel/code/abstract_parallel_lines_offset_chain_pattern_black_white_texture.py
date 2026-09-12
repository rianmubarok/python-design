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
def abstract_parallel_lines_offset_chain_pattern_black_white_texture():
    """Garis paralel dengan offset berantai"""
    fig, ax = setup_ax()
    n_lines = 50
    for i in range(n_lines):
        y = -5 + i * 2.2
        offset = 8 * np.sin(i * 0.6)
        seg_len = 15
        x = -5
        while x < 105:
            x_end = min(x + seg_len, 105)
            lw = np.random.choice([2.0, 3.0])
            ax.plot([-5, 105], [y, y], color="black", linewidth=lw)
            x = x_end + 5
            offset = -offset
    save(fig, "abstract_parallel_lines_offset_chain_pattern_black_white_texture")


if __name__ == "__main__":
    abstract_parallel_lines_offset_chain_pattern_black_white_texture()
