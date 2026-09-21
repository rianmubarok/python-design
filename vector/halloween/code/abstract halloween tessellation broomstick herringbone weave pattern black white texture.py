import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (
    Arc, Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle,
)
from matplotlib.transforms import Affine2D
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
    ax.set_clip_on(True)
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")

def broom(ax, cx, cy, ang):
    tr = Affine2D().rotate_deg(ang).translate(cx, cy) + ax.transData
    ax.plot([-5.2, 1.8], [0, 0], color="black", linewidth=1.25, solid_capstyle="round", transform=tr)
    for k in np.linspace(-0.95, 0.95, 9):
        ax.plot([1.6, 5.1], [0, k], color="black", linewidth=0.5, transform=tr)
    ax.plot([1.4, 1.4], [-0.55, 0.55], color="black", linewidth=1.1, transform=tr)


def draw():
    """Seamless broomstick herringbone."""
    fig, ax = setup_ax()
    cols, rows = 12, 12
    dx, dy = PERIOD / cols, PERIOD / rows
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy + (dy * 0.5 if col % 2 else 0)
            ang = 40 if col % 2 == 0 else -40
            for ox, oy in WRAPS:
                broom(ax, cx + ox, cy + oy, ang)
    save(fig, "abstract halloween tessellation broomstick herringbone weave pattern black white texture")


if __name__ == "__main__":
    draw()
