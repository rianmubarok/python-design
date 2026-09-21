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

def star(cx, cy, r, n=5, inner=0.4):
    pts = []
    for i in range(n * 2):
        ang = -np.pi / 2 + i * np.pi / n
        rad = r if i % 2 == 0 else r * inner
        pts.append([cx + rad * np.cos(ang), cy + rad * np.sin(ang)])
    return np.array(pts)


def draw():
    """Seamless moon and star checker lattice."""
    fig, ax = setup_ax()
    n = 8
    step = PERIOD / n
    for row in range(n):
        for col in range(n):
            cx = (col + 0.5) * step
            cy = (row + 0.5) * step
            for ox, oy in WRAPS:
                x, y = cx + ox, cy + oy
                if (row + col) % 2 == 0:
                    ax.add_patch(Circle((x, y), 4.15, facecolor="black", edgecolor="none"))
                    ax.add_patch(Circle((x + 1.25, y + 0.35), 3.35, facecolor="white", edgecolor="none"))
                else:
                    ax.add_patch(Polygon(star(x, y, 3.05), closed=True, facecolor="black", edgecolor="none"))
                    ax.add_patch(Polygon(star(x, y, 1.2, inner=0.45), closed=True, facecolor="white", edgecolor="none"))
    save(fig, "abstract halloween tessellation crescent moon star lattice pattern black white texture")


if __name__ == "__main__":
    draw()
