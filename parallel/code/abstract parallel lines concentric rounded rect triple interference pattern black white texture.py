import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.transforms import Affine2D
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


def family(ax, angle, n_rects, spacing, base_half, lw):
    tr = Affine2D().rotate_deg_around(50.0, 50.0, angle) + ax.transData
    for i in range(n_rects):
        half = base_half - i * spacing
        if half <= 1:
            break
        r = 0.18 * (2 * half)
        box = FancyBboxPatch(
            (50.0 - half, 50.0 - half),
            half * 2,
            half * 2,
            boxstyle=f"round,pad=0,rounding_size={r}",
            fill=False,
            edgecolor="black",
            linewidth=lw,
            transform=tr,
        )
        ax.add_patch(box)


def abstract_parallel_lines_concentric_rounded_rect_triple_interference_pattern_black_white_texture():
    """Wild combo: rounded rect x moire x rosette -- three rotated families interleave"""
    fig, ax = setup_ax()
    family(ax, 0.0, 20, 2.6, 50.0, 0.85)
    family(ax, 60.0, 15, 2.3, 35.0, 0.55)
    family(ax, 120.0, 15, 2.3, 35.0, 0.55)
    save(fig, "abstract parallel lines concentric rounded rect triple interference pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_concentric_rounded_rect_triple_interference_pattern_black_white_texture()
