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
def parallel_stepped():
    fig, ax = setup_ax()
    n_lines = 25
    n_steps = 10
    step_width = 110 / n_steps
    for i in range(n_lines):
        y_base = -5 + i * (110 / n_lines)
        for j in range(n_steps):
            x_start = -5 + j * step_width
            x_end = x_start + step_width
            y_offset = (j % 2) * 2
            ax.plot([x_start, x_end], [y_base + y_offset, y_base + y_offset],
                    color="black", linewidth=0.6)
            if j < n_steps - 1:
                ax.plot([x_end, x_end], [y_base + y_offset, y_base + (j + 1) % 2 * 2],
                        color="black", linewidth=0.6)
    save(fig, "parallel_stepped")


if __name__ == "__main__":
    parallel_stepped()
