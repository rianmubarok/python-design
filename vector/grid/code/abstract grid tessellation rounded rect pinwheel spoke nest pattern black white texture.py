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
    """Rounded-rect grid with nested boxes and rotating pinwheel spokes."""
    fig, ax = setup_ax()
    n = 7
    cell = 100 / n
    for r in range(n):
        for c in range(n):
            cx, cy = (c + 0.5) * cell, (r + 0.5) * cell
            rnd = 1.1 + 1.6 * (0.5 + 0.5 * np.sin(c * 0.9) * np.cos(r * 0.7))
            for k in range(4):
                w = cell * (0.86 - k * 0.16)
                ax.add_patch(FancyBboxPatch((cx - w / 2, cy - w / 2), w, w,
                                            boxstyle=f"round,pad=0,rounding_size={rnd * (1 - k * 0.12)}",
                                            fill=False, edgecolor="black", linewidth=1.05 - k * 0.18))
            spin = np.deg2rad(18 * (c - r) + 12 * np.sin(c + r))
            rad = cell * 0.28
            for i in range(6):
                ang = spin + i * np.pi / 3
                ax.plot([cx, cx + rad * np.cos(ang)], [cy, cy + rad * np.sin(ang)],
                        color="black", linewidth=0.7)
    save(fig, "abstract grid tessellation rounded rect pinwheel spoke nest pattern black white texture")


if __name__ == "__main__":
    draw()
