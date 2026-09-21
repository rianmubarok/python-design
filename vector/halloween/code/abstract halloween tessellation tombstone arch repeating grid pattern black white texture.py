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

def stone(ax, cx, cy, w, h):
    x0, y0 = cx - w / 2, cy - h / 2
    ax.add_patch(Rectangle((x0, y0), w, h * 0.62, facecolor="none", edgecolor="black", linewidth=1.15))
    ax.add_patch(Arc((cx, y0 + h * 0.62), w, w * 0.95, theta1=0, theta2=180, color="black", linewidth=1.15))
    ax.add_patch(Rectangle((x0 + 0.55, y0 + 0.55), w - 1.1, h * 0.4, fill=False, edgecolor="black", linewidth=0.45))
    ax.plot([cx, cx], [cy - 1.15, cy + 1.85], color="black", linewidth=1.45)
    ax.plot([cx - 1.45, cx + 1.45], [cy + 0.7, cy + 0.7], color="black", linewidth=1.45)


def draw():
    """Seamless staggered tombstone grid."""
    fig, ax = setup_ax()
    cols, rows = 8, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    w, h = dx * 0.62, dy * 0.72
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                stone(ax, cx + ox, cy + oy, w, h)
    save(fig, "abstract halloween tessellation tombstone arch repeating grid pattern black white texture")


if __name__ == "__main__":
    draw()
