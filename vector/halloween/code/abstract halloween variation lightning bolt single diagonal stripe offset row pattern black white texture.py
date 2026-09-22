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


def lightning_bolt(ax, cx, cy, h, w, angle_deg=45.0, fill="white"):
    a = np.radians(angle_deg)
    c, s = np.cos(a), np.sin(a)
    pts_local = np.array([
        [ 0.10 * w,  0.50 * h],
        [ 0.00 * w,  0.05 * h],
        [ 0.35 * w,  0.05 * h],
        [-0.10 * w, -0.50 * h],
        [ 0.00 * w, -0.05 * h],
        [-0.35 * w, -0.05 * h],
    ])
    R = np.array([[c, -s], [s, c]])
    pts = (R @ pts_local.T).T + [cx, cy]
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor="none"))


def draw():
    """Single-direction diagonal lightning bolts arranged in brick-offset rows.
    Each row is staggered by half a cell, creating a diagonal cascade stripe.
    Uniform 45° angle throughout — no crosshatch, pure directional stripe.
    """
    fig, ax = setup_ax()
    cols, rows = 6, 8
    dx = PERIOD / cols
    dy = PERIOD / rows
    bh = dy * 1.10
    bw = dx * 0.48

    for row in range(rows):
        shift = dx * 0.5 if row % 2 else 0.0
        for col in range(cols):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                lightning_bolt(ax, cx + ox, cy + oy, bh, bw, angle_deg=45, fill="white")

    save(fig,
         "abstract halloween variation lightning bolt single diagonal stripe "
         "offset row pattern black white texture")


if __name__ == "__main__":
    draw()
