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
    """Truchet arcs squashed into ellipses with a drifting tile offset."""
    fig, ax = setup_ax()
    n = 14
    cell = 100 / n
    rng = np.random.default_rng(21)
    for row in range(n):
        for col in range(n):
            ox = 0.18 * cell * np.sin(row * 0.55)
            oy = 0.18 * cell * np.cos(col * 0.5)
            x0 = col * cell + ox
            y0 = row * cell + oy
            sx = 0.72 + 0.45 * (0.5 + 0.5 * np.sin(col * 0.4))
            sy = 0.72 + 0.45 * (0.5 + 0.5 * np.cos(row * 0.4))
            rot = int(rng.integers(0, 2))
            for k, f in enumerate((0.28, 0.58, 0.88)):
                ww, hh = cell * f * sx * 2, cell * f * sy * 2
                lw = 1.15 - k * 0.25
                if rot == 0:
                    ax.add_patch(Arc((x0, y0 + cell), ww, hh, theta1=270, theta2=360, color="black", linewidth=lw))
                    ax.add_patch(Arc((x0 + cell, y0), ww, hh, theta1=90, theta2=180, color="black", linewidth=lw))
                else:
                    ax.add_patch(Arc((x0, y0), ww, hh, theta1=0, theta2=90, color="black", linewidth=lw))
                    ax.add_patch(Arc((x0 + cell, y0 + cell), ww, hh, theta1=180, theta2=270, color="black", linewidth=lw))
    save(fig, "abstract grid tessellation truchet ellipse squash drift pattern black white texture")


if __name__ == "__main__":
    draw()
