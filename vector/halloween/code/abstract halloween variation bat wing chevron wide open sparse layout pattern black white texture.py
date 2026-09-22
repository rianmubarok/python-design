import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI  = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR  = SCRIPT_DIR.parent / "output"
JPG_DIR     = OUTPUT_DIR / "jpg"
SVG_DIR     = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("black")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="black")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="black")
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def draw_bat_wide(ax, cx, cy, w, h, fill="white"):
    """Wide-wingspan geometric bat chevron — elongated outer wing panels."""
    polygons = []

    # Center diamond (body)
    polygons.append([
        ( 0.00 * w,  0.38 * h),
        ( 0.08 * w,  0.08 * h),
        ( 0.00 * w, -0.25 * h),
        (-0.08 * w,  0.08 * h),
    ])

    def sym(poly):
        polygons.append(poly)
        polygons.append([(-x, y) for x, y in poly])

    # Inner wing panel — stretched outward
    sym([
        ( 0.12 * w,  0.22 * h),
        ( 0.22 * w, -0.05 * h),
        ( 0.22 * w, -0.42 * h),
        ( 0.12 * w, -0.18 * h),
    ])
    # Mid wing panel
    sym([
        ( 0.26 * w,  0.02 * h),
        ( 0.40 * w, -0.22 * h),
        ( 0.40 * w, -0.50 * h),
        ( 0.26 * w, -0.26 * h),
    ])
    # Outer long wing tip
    sym([
        ( 0.44 * w, -0.10 * h),
        ( 0.58 * w, -0.32 * h),
        ( 0.44 * w, -0.44 * h),
    ])
    # Thumb claw nub
    sym([
        ( 0.60 * w, -0.15 * h),
        ( 0.68 * w, -0.28 * h),
        ( 0.60 * w, -0.34 * h),
    ])

    for poly in polygons:
        shifted = [(px + cx, py + cy) for px, py in poly]
        for ox, oy in WRAPS:
            final = [(px + ox, py + oy) for px, py in shifted]
            ax.add_patch(Polygon(final, facecolor=fill, edgecolor="none", zorder=2))


def draw():
    """Sparse open grid of wide-wingspan bat chevrons — 6 cols × 7 rows.
    White bats on black background with staggered brick offset.
    """
    fig, ax = setup_ax()
    cols, rows = 6, 7
    dx = PERIOD / cols
    dy = PERIOD / rows
    w = dx * 1.15   # wider than cell to create overlap
    h = dy * 1.10

    for row in range(rows):
        shift = dx * 0.5 if row % 2 else 0.0
        for col in range(cols):
            cx = col * dx + shift
            cy = (row + 0.5) * dy
            draw_bat_wide(ax, cx, cy, w, h, fill="white")

    save(fig,
         "abstract halloween variation bat wing chevron wide open sparse layout "
         "pattern black white texture")


if __name__ == "__main__":
    draw()
