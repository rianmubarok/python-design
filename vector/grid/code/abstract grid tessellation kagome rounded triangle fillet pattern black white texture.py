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
    """Kagome dual triangles with filleted (rounded) corners."""
    fig, ax = setup_ax()
    scale = 7.0
    h = scale * np.sqrt(3) / 2

    def round_tri(cx, cy, r, off, nseg=6):
        angs = np.deg2rad(np.array([off, off + 120, off + 240]))
        pts = np.column_stack([cx + r * np.cos(angs), cy + r * np.sin(angs)])
        curve = []
        for i in range(3):
            p0, p1, p2 = pts[i], pts[(i + 1) % 3], pts[(i + 2) % 3]
            a0 = p0 * 0.22 + p1 * 0.78
            a1 = p1 * 0.78 + p2 * 0.22
            for t in np.linspace(0, 1, nseg, endpoint=False):
                curve.append((1 - t) ** 2 * a0 + 2 * (1 - t) * t * p1 + t ** 2 * a1)
        return np.array(curve)

    for row in range(-2, 16):
        for col in range(-2, 16):
            cx = col * scale * 1.5
            cy = row * h * 2 + (h if col % 2 else 0)
            r = scale * 0.78 * (0.9 + 0.12 * np.sin(col * 0.4))
            ax.add_patch(Polygon(round_tri(cx, cy, r, 90), closed=True, fill=False,
                                 edgecolor="black", linewidth=1.2))
            ax.add_patch(Polygon(round_tri(cx, cy, r, 270), closed=True, fill=False,
                                 edgecolor="black", linewidth=1.2))
    save(fig, "abstract grid tessellation kagome rounded triangle fillet pattern black white texture")


if __name__ == "__main__":
    draw()
