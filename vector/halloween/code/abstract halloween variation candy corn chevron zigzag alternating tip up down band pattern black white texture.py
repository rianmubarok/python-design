import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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


def draw_candy_corn(ax, cx, cy, h, w_base, flip=False, fill="white", mid="gray"):
    """Triangle candy corn. flip=True points downward."""
    sign = -1.0 if flip else 1.0
    tip_y = cy + sign * h * 0.5
    base_y = cy - sign * h * 0.5
    mid_y1 = cy - sign * h * 0.10
    mid_y2 = cy - sign * h * 0.38

    w_mid = w_base * 0.60
    w_tip = 0.0

    # Base band
    base_pts = [
        [cx - w_base / 2, base_y],
        [cx + w_base / 2, base_y],
        [cx + w_mid / 2, mid_y1],
        [cx - w_mid / 2, mid_y1],
    ]
    # Mid band
    mid_pts = [
        [cx - w_mid / 2, mid_y1],
        [cx + w_mid / 2, mid_y1],
        [cx + w_base * 0.18, mid_y2],
        [cx - w_base * 0.18, mid_y2],
    ]
    # Tip band
    tip_pts = [
        [cx - w_base * 0.18, mid_y2],
        [cx + w_base * 0.18, mid_y2],
        [cx, tip_y],
    ]

    ax.add_patch(Polygon(base_pts, closed=True, facecolor=fill, edgecolor="none"))
    ax.add_patch(Polygon(mid_pts,  closed=True, facecolor=mid,  edgecolor="none"))
    ax.add_patch(Polygon(tip_pts,  closed=True, facecolor=fill, edgecolor="none"))


def draw():
    """Chevron rows of candy corn. Even rows tip-up, odd rows tip-down (flip).
    Columns are offset to create a chevron/zigzag band pattern.
    Black background, white candy corn with grey mid-band."""
    fig, ax = setup_ax()

    cols, rows = 8, 10
    dx, dy = PERIOD / cols, PERIOD / rows
    h = dy * 0.88
    w = dx * 0.76

    for row in range(-1, rows + 1):
        flip = bool(row % 2)
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -10 <= px <= PERIOD + 10 and -10 <= py <= PERIOD + 10:
                    draw_candy_corn(ax, px, py, h, w,
                                   flip=flip, fill="white", mid="#777777")

    save(fig, "abstract halloween variation candy corn chevron zigzag alternating tip up down band pattern black white texture")


if __name__ == "__main__":
    draw()
