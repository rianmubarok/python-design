import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (
    Arc, Circle, Ellipse, FancyBboxPatch, Polygon, RegularPolygon,
)
from matplotlib.transforms import Affine2D
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

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


def squircle(cx, cy, rx, ry, p, n=72):
    t = np.linspace(0, 2 * np.pi, n)
    ct, st = np.cos(t), np.sin(t)
    x = cx + rx * np.sign(ct) * (np.abs(ct) ** (2 / p))
    y = cy + ry * np.sign(st) * (np.abs(st) ** (2 / p))
    return x, y

def draw():
    """Chainmail ellipses locked onto hexagonal nodes with a squash wave."""
    fig, ax = setup_ax()
    r = 4.6
    dx, dy = r * np.sqrt(3), r * 1.5
    for row in range(-2, 22):
        for col in range(-2, 18):
            cx = col * dx + (dx / 2 if row % 2 else 0)
            cy = row * dy
            squash = 0.58 + 0.28 * (0.5 + 0.5 * np.sin(col * 0.35) * np.cos(row * 0.28))
            ang = 18 if row % 2 == 0 else -18
            ax.add_patch(Ellipse((cx, cy), r * 2.05, r * 2.05 * squash, angle=ang,
                                 fill=False, edgecolor="black", linewidth=1.05))
            ax.add_patch(Circle((cx, cy), r * 0.18, fill=False, edgecolor="black", linewidth=0.4))
    save(fig, "abstract grid tessellation chainmail hex node lock pattern black white texture")


if __name__ == "__main__":
    draw()
