import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def draw_bat(ax, cx, cy, w, h, fill="black", flip=False):
    """Geometric bat. flip=True mirrors vertically (wings point down)."""
    fy = -1 if flip else 1

    body = [(0, fy * 0.18 * h), (0.07 * w, fy * 0.06 * h),
            (0, fy * -0.10 * h), (-0.07 * w, fy * 0.06 * h)]

    lwing = [
        (0,          fy * 0.10 * h),
        (-0.20 * w,  fy * 0.24 * h),
        (-0.40 * w,  fy * 0.10 * h),
        (-0.44 * w,  fy * -0.12 * h),
        (-0.28 * w,  fy * -0.18 * h),
        (-0.14 * w,  fy * -0.05 * h),
        (0,          0.0),
    ]
    rwing = [(-px, py) for px, py in lwing]

    for poly in [body, lwing, rwing]:
        pts = [(cx + px, cy + py) for px, py in poly]
        ax.add_patch(Polygon(pts, closed=True, facecolor=fill,
                             edgecolor="none", zorder=2))


def draw():
    """Horizontal stripe rows of bats.
    Even rows  → black background stripe, white bats flying normally (wings up).
    Odd rows   → white background stripe, black bats flipped (wings down / inverted).
    Bats are horizontally staggered (brick shift) between rows. Seamless."""
    fig, ax = setup_ax()

    rows = 7
    cols = 6
    dy = PERIOD / rows
    dx = PERIOD / cols
    w = dx * 0.92
    h = dy * 0.72

    for row in range(rows):
        bg    = "black" if row % 2 == 0 else "white"
        fill  = "white" if bg == "black"  else "black"
        flip  = (row % 2 != 0)            # alternate flying direction

        for ox, oy in WRAPS:
            ax.add_patch(Rectangle(
                (0 + ox, row * dy + oy), PERIOD, dy,
                facecolor=bg, edgecolor="none", zorder=0))

        shift = (dx * 0.5) if row % 2 else 0.0
        cy = (row + 0.5) * dy

        for col in range(-1, cols + 2):
            cx = col * dx + shift + dx * 0.5
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -5 <= py <= PERIOD + 5:
                    draw_bat(ax, px, py, w, h, fill=fill, flip=flip)

    save(fig, "abstract halloween variation bat chevron inverted alternating row direction pattern black white texture")


if __name__ == "__main__":
    draw()
