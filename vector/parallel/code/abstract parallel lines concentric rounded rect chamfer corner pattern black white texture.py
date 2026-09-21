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


def abstract_parallel_lines_concentric_rounded_rect_chamfer_corner_pattern_black_white_texture():
    """Tweak: round corners replaced by 45 degree cuts that grow as the rings close in"""
    fig, ax = setup_ax()
    n_rects = 30
    for i in range(n_rects):
        margin = i * 1.7
        w = 100 - 2 * margin
        if w <= 2:
            break
        t = i / (n_rects - 1)
        c = w * (0.04 + 0.28 * t)
        x0, y0 = margin, margin
        x1, y1 = margin + w, margin + w
        xs = [x0 + c, x1 - c, x1, x1, x1 - c, x0 + c, x0, x0]
        ys = [y0, y0, y0 + c, y1 - c, y1, y1, y1 - c, y0 + c]
        lw = 0.6 + 0.4 * (1 - t)
        ax.plot(xs + [xs[0]], ys + [ys[0]], color="black", linewidth=lw,
                solid_joinstyle="miter")
    save(fig, "abstract parallel lines concentric rounded rect chamfer corner pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_concentric_rounded_rect_chamfer_corner_pattern_black_white_texture()
