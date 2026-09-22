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


def draw_bolt(ax, cx, cy, w, h, fill="white", flip=False):
    """Classic Frankenstein lightning bolt silhouette.
    flip=True → bolt points downward instead of upward."""
    fy = -1 if flip else 1
    # Bolt points: a thick angular Z-shape
    pts = [
        (cx - w * 0.20, cy + fy * h * 0.50),   # top-left
        (cx + w * 0.38, cy + fy * h * 0.50),   # top-right
        (cx + w * 0.04, cy + fy * h * 0.04),   # centre-right
        (cx + w * 0.36, cy + fy * h * 0.04),   # mid-right shelf
        (cx - w * 0.20, cy - fy * h * 0.50),   # bottom-right
        (cx - w * 0.38, cy - fy * h * 0.50),   # bottom-left
        (cx - w * 0.04, cy - fy * h * 0.04),   # centre-left
        (cx - w * 0.36, cy - fy * h * 0.04),   # mid-left shelf
    ]
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill,
                         edgecolor="none", zorder=2))


def draw():
    """Horizontal stripe rows, alternating black/white bands.
    Even rows → black stripe, white lightning bolts pointing up.
    Odd rows  → white stripe, black lightning bolts pointing down (flipped).
    Bolt columns are brick-offset between rows. Seamless."""
    fig, ax = setup_ax()

    rows = 7
    cols = 6
    dy = PERIOD / rows
    dx = PERIOD / cols
    w  = dx * 0.78
    h  = dy * 0.72

    for row in range(rows):
        bg   = "black" if row % 2 == 0 else "white"
        fill = "white" if bg == "black"  else "black"
        flip = (row % 2 != 0)

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
                    draw_bolt(ax, px, py, w, h, fill=fill, flip=flip)

    save(fig, "abstract halloween variation lightning bolt zigzag brick fill alternating dark light rows pattern black white texture")


if __name__ == "__main__":
    draw()
