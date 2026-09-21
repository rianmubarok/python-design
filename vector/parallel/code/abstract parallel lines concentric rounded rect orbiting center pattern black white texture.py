import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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


def abstract_parallel_lines_concentric_rounded_rect_orbiting_center_pattern_black_white_texture():
    """Tweak: nesting center jumps a quarter turn each ring, so the frames orbit inward"""
    fig, ax = setup_ax()
    n_rects = 30
    for i in range(n_rects):
        t = i / (n_rects - 1)
        half = 48.0 - i * 1.6
        if half <= 1:
            break
        orbit = 5.5 * (1 - t)
        ang = i * np.pi / 2
        cx = 50.0 + orbit * np.cos(ang)
        cy = 50.0 + orbit * np.sin(ang)
        r = 0.22 * (2 * half)
        box = FancyBboxPatch(
            (cx - half, cy - half),
            half * 2,
            half * 2,
            boxstyle=f"round,pad=0,rounding_size={r}",
            fill=False,
            edgecolor="black",
            linewidth=0.6 + 0.4 * (1 - t),
        )
        ax.add_patch(box)
    save(fig, "abstract parallel lines concentric rounded rect orbiting center pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_concentric_rounded_rect_orbiting_center_pattern_black_white_texture()
