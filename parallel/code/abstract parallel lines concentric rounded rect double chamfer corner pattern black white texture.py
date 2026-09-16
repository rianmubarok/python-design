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


def double_chamfer_rect(x0, y0, x1, y1, c, m):
    """Closed outline of a rectangle whose four corners are two-step staircases."""
    pts = [
        (x0 + c, y0),
        (x1 - c, y0),
        (x1 - c + m, y0), (x1 - c + m, y0 + m), (x1, y0 + m), (x1, y0 + c),
        (x1, y1 - c),
        (x1 - m, y1 - c), (x1 - m, y1 - c + m), (x1 - c, y1 - c + m), (x1 - c, y1),
        (x0 + c, y1),
        (x0 + c - m, y1), (x0 + c - m, y1 - m), (x0, y1 - m), (x0, y1 - c),
        (x0, y0 + c),
        (x0, y0 + c - m), (x0 + m, y0 + c - m), (x0 + m, y0), (x0 + c, y0),
    ]
    xs, ys = zip(*pts)
    return list(xs), list(ys)


def abstract_parallel_lines_concentric_rounded_rect_double_chamfer_corner_pattern_black_white_texture():
    """Tweak: each chamfer is cut again, giving corners a two-step staircase"""
    fig, ax = setup_ax()
    n_rects = 30
    for i in range(n_rects):
        margin = i * 1.7
        w = 100 - 2 * margin
        if w <= 2:
            break
        t = i / (n_rects - 1)
        c = w * (0.05 + 0.24 * t)
        m = 0.55 * c
        xs, ys = double_chamfer_rect(margin, margin, margin + w, margin + w, c, m)
        lw = 0.6 + 0.4 * (1 - t)
        ax.plot(xs, ys, color="black", linewidth=lw, solid_joinstyle="miter")
    save(fig, "abstract parallel lines concentric rounded rect double chamfer corner pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_concentric_rounded_rect_double_chamfer_corner_pattern_black_white_texture()
