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


def abstract_parallel_lines_organic_flow_pattern_black_white_texture():
    """Garis paralel mengalir organik"""
    fig, ax = setup_ax()
    n_lines = 40
    for i in range(n_lines):
        y_base = -5 + i * 2.8
        x = np.linspace(-5, 105, 200)
        flow = 10 * np.sin(x * 0.05 + i * 0.4) * np.cos(x * 0.03 - i * 0.2)
        y = y_base + flow
        lw = 1.5 + 1.5 * np.abs(np.sin(i * 0.3))
        ax.plot(x, y, color="black", linewidth=lw)
    save(fig, "abstract parallel lines organic flow pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_organic_flow_pattern_black_white_texture()
