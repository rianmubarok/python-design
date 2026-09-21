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
    """Isometric cubes with a staircase-like vertical offset wave."""
    fig, ax = setup_ax()
    cube = 5.0
    h = cube * np.sqrt(3) / 2
    for row in range(-2, 18):
        for col in range(-2, 18):
            s = cube
            lift = 2.4 * np.sin(col * 0.45) + 1.6 * np.cos(row * 0.35)
            cx = col * cube * 1.5
            cy = row * h * 2 + (h if col % 2 else 0) + lift
            p1 = np.array([0, s]); p2 = np.array([s * np.cos(np.pi / 6), s * np.sin(np.pi / 6)])
            p3 = np.array([s * np.cos(np.pi / 6), -s * np.sin(np.pi / 6)]); p4 = np.array([0, -s])
            p5 = np.array([-s * np.cos(np.pi / 6), -s * np.sin(np.pi / 6)])
            p6 = np.array([-s * np.cos(np.pi / 6), s * np.sin(np.pi / 6)])
            o = np.array([cx, cy])
            ax.add_patch(Polygon(o + np.array([p1, p2, p3, [0, 0]]), closed=True,
                                 facecolor="white", edgecolor="black", linewidth=0.95))
            ax.add_patch(Polygon(o + np.array([[0, 0], p3, p4, p5]), closed=True,
                                 facecolor="none", edgecolor="black", linewidth=0.95, hatch="///"))
            ax.add_patch(Polygon(o + np.array([[0, 0], p5, p6, p1]), closed=True,
                                 facecolor="black", edgecolor="black", linewidth=0.95))
    save(fig, "abstract grid tessellation isometric cube staircase height wave pattern black white texture")


if __name__ == "__main__":
    draw()
