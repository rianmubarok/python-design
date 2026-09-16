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


def abstract_parallel_lines_nested_rounded_rect_offcenter_drift_pattern_black_white_texture():
    """Tweak: nesting center slides diagonally so ring spacing opens on one side"""
    fig, ax = setup_ax()
    n_rects = 30
    outer_cx, outer_cy = 50.0, 50.0
    drift_cx, drift_cy = 70.0, 30.0
    for i in range(n_rects):
        t = i / (n_rects - 1)
        cx = outer_cx + (drift_cx - outer_cx) * t
        cy = outer_cy + (drift_cy - outer_cy) * t
        half = 54.0 * (1 - 0.90 * t)
        r = min(0.5 + 6.0 * (1 - t), 0.42 * half)
        lw = 0.6 + 0.5 * (1 - t)
        box = FancyBboxPatch(
            (cx - half, cy - half),
            half * 2,
            half * 2,
            boxstyle=f"round,pad=0,rounding_size={r}",
            fill=False,
            edgecolor="black",
            linewidth=lw,
        )
        ax.add_patch(box)
    save(fig, "abstract parallel lines nested rounded rect offcenter drift pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_nested_rounded_rect_offcenter_drift_pattern_black_white_texture()
