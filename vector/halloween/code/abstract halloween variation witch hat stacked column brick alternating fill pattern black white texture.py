import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, FancyBboxPatch
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


def witch_hat(ax, cx, cy, w, h, fill="black"):
    """Witch hat: triangular cone + wide flat brim.
    fill='black' → solid black hat.
    fill='white' → white hat with black outline.
    """
    inv  = "white" if fill == "black" else "black"
    edge = "none"  if fill == "black" else "black"
    elw  = 0.0     if fill == "black" else 1.2

    # Cone (triangle with slight curve — 3 pts suffice as polygon)
    tip_x  = cx
    tip_y  = cy + h * 0.50
    base_y = cy - h * 0.08
    cone_pts = [
        (cx - w * 0.25, base_y),
        (tip_x,         tip_y),
        (cx + w * 0.25, base_y),
    ]
    ax.add_patch(Polygon(cone_pts, closed=True,
                         facecolor=fill, edgecolor=edge, linewidth=elw))

    # Brim (wide flat ellipse)
    brim_cx, brim_cy = cx, cy - h * 0.14
    ax.add_patch(Ellipse((brim_cx, brim_cy), w * 0.96, h * 0.18,
                         facecolor=fill, edgecolor=edge, linewidth=elw))

    # Hat band — thin strip just above brim
    band_y = cy - h * 0.08
    ax.add_patch(FancyBboxPatch(
        (cx - w * 0.245, band_y), w * 0.49, h * 0.060,
        boxstyle="square,pad=0",
        facecolor=inv, edgecolor="none"))


def draw():
    """Brick-offset column grid of witch hats.
    Odd columns shift up by half a cell.
    Alternating black/white fill per (row + col) parity — checkerboard on a brick grid.
    White background.
    """
    fig, ax = setup_ax()
    cols, rows = 6, 7
    dx, dy = PERIOD / cols, PERIOD / rows
    w = dx * 0.88
    h = dy * 0.88

    for col in range(cols):
        shift = dy * 0.5 if col % 2 else 0.0
        for row in range(rows):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy + shift
            fill = "black" if (row + col) % 2 == 0 else "white"
            for ox, oy in WRAPS:
                witch_hat(ax, cx + ox, cy + oy, w, h, fill=fill)

    save(fig,
         "abstract halloween variation witch hat stacked column brick "
         "alternating fill pattern black white texture")


if __name__ == "__main__":
    draw()
