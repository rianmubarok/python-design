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


def abstract_parallel_lines_nested_rounded_rect_tunnel_perspective_pattern_black_white_texture():
    """Tweak: rounded corners applied to the perspective tunnel, radius deepens inward"""
    fig, ax = setup_ax()
    n_rects = 38
    target_cx, target_cy = 28.0, 72.0
    outer_cx, outer_cy = 50.0, 50.0

    for i in range(n_rects):
        t = i / (n_rects - 1)
        cx = (1 - t) * outer_cx + t * target_cx
        cy = (1 - t) * outer_cy + t * target_cy

        half_w = 54.0 * (1 - t * 0.94)
        half_h = 54.0 * (1 - t * 0.94)
        lw = 1.0 + 2.6 * ((1 - t) ** 1.2)
        r = min(1.0 + 9.0 * t, 0.45 * min(half_w, half_h) * 2)

        box = FancyBboxPatch(
            (cx - half_w, cy - half_h),
            half_w * 2,
            half_h * 2,
            boxstyle=f"round,pad=0,rounding_size={r}",
            fill=False,
            edgecolor="black",
            linewidth=lw,
        )
        ax.add_patch(box)

    save(fig, "abstract parallel lines nested rounded rect tunnel perspective pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_nested_rounded_rect_tunnel_perspective_pattern_black_white_texture()
