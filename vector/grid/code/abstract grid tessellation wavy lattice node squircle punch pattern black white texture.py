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
    """Sine-sheared lattice with squircle punches at every intersection."""
    fig, ax = setup_ax()
    n = 18
    pts = np.linspace(-8, 108, 180)
    xs = np.linspace(-8, 108, n)
    for i, x0 in enumerate(xs):
        ax.plot(x0 + 3.2 * np.sin(pts * 0.11 + i * 0.2), pts, color="black", linewidth=0.75)
    for j, y0 in enumerate(xs):
        ax.plot(pts, y0 + 3.2 * np.sin(pts * 0.11 + j * 0.2), color="black", linewidth=0.75)
    for i, x0 in enumerate(xs):
        for j, y0 in enumerate(xs):
            cx = x0 + 3.2 * np.sin(y0 * 0.11 + i * 0.2)
            cy = y0 + 3.2 * np.sin(x0 * 0.11 + j * 0.2)
            p = 2.2 + 4.0 * (0.5 + 0.5 * np.sin(i * 0.4) * np.cos(j * 0.35))
            r = 1.05 + 0.55 * (0.5 + 0.5 * np.cos(i + j))
            xx, yy = squircle(cx, cy, r, r, p, 40)
            ax.plot(xx, yy, color="black", linewidth=0.85)
    save(fig, "abstract grid tessellation wavy lattice node squircle punch pattern black white texture")


if __name__ == "__main__":
    draw()
