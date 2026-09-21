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
    """Halftone dots locked onto a hexagonal lattice with a radial pulse."""
    fig, ax = setup_ax()
    r = 4.2
    dx, dy = r * np.sqrt(3), r * 1.5
    ox, oy = 50.0, 50.0
    for row in range(22):
        for col in range(22):
            cx = col * dx + (dx / 2 if row % 2 else 0) - 8
            cy = row * dy - 8
            dist = np.hypot(cx - ox, cy - oy)
            rad = 0.25 + 1.85 * (0.5 + 0.5 * np.sin(dist * 0.18 + col * 0.1))
            ax.add_patch(Circle((cx, cy), rad, facecolor="black", edgecolor="none"))
            ax.add_patch(RegularPolygon((cx, cy), 6, radius=r * 0.92, orientation=0,
                                        fill=False, edgecolor="black", linewidth=0.25))
    fit_view(ax, pad=48)
    save(fig, "abstract grid tessellation halftone hex lattice radius pulse pattern black white texture")


if __name__ == "__main__":
    draw()
