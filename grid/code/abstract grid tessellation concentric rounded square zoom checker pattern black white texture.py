import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (
    Arc, Circle, Ellipse, FancyBboxPatch, Polygon, RegularPolygon, Rectangle, PathPatch,
)
from matplotlib.path import Path as MplPath
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


def fit_view(ax, pad=55):
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)


def squircle(cx, cy, rx, ry, p, n=80):
    t = np.linspace(0, 2 * np.pi, n)
    ct, st = np.cos(t), np.sin(t)
    x = cx + rx * np.sign(ct) * (np.abs(ct) ** (2 / p))
    y = cy + ry * np.sign(st) * (np.abs(st) ** (2 / p))
    return x, y

def draw():
    """Concentric rounded squares with a checkerboard zoom and corner-radius flip."""
    fig, ax = setup_ax()
    n = 6
    cell = 100 / n
    for r in range(n):
        for c in range(n):
            cx, cy = (c + 0.5) * cell, (r + 0.5) * cell
            zoom = 1.12 if (r + c) % 2 == 0 else 0.82
            rings = 5 if (r + c) % 2 == 0 else 3
            for k in range(rings):
                w = cell * zoom * (0.86 - k * 0.14)
                rnd = (0.42 * w) if (r + c + k) % 2 == 0 else (0.12 * w)
                ax.add_patch(FancyBboxPatch((cx - w / 2, cy - w / 2), w, w,
                                            boxstyle=f"round,pad=0,rounding_size={max(rnd, 0.2)}",
                                            fill=False, edgecolor="black", linewidth=1.05 - k * 0.12))
    save(fig, "abstract grid tessellation concentric rounded square zoom checker pattern black white texture")


if __name__ == "__main__":
    draw()
