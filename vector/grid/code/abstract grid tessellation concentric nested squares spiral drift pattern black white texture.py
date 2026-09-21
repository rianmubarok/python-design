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
    """Nested squares that spiral in rotation and drift off-center per cell."""
    fig, ax = setup_ax()
    n = 6
    cell = 100 / n
    for r in range(n):
        for c in range(n):
            cx = (c + 0.5) * cell + 1.6 * np.sin(r * 0.8)
            cy = (r + 0.5) * cell + 1.6 * np.cos(c * 0.8)
            for k in range(7):
                w = cell * (0.88 - k * 0.11)
                ang = np.deg2rad(k * (7 + 3 * np.sin(c + r)))
                ca, sa = np.cos(ang), np.sin(ang)
                half = w / 2
                corners = np.array([[-half, -half], [half, -half], [half, half], [-half, half]])
                rot = corners @ np.array([[ca, sa], [-sa, ca]])
                ax.add_patch(Polygon(rot + [cx, cy], closed=True, fill=False,
                                     edgecolor="black", linewidth=0.95))
    save(fig, "abstract grid tessellation concentric nested squares spiral drift pattern black white texture")


if __name__ == "__main__":
    draw()
