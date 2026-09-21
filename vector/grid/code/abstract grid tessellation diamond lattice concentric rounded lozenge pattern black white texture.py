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
    """45-degree diamond lattice with concentric rounded lozenges."""
    fig, ax = setup_ax()
    step = 9.0
    for row in range(-2, 16):
        for col in range(-2, 16):
            cx = col * step
            cy = row * step + (step / 2 if col % 2 else 0)
            for k, sc in enumerate((1.0, 0.66, 0.36)):
                w = step * 0.46 * sc
                h = step * 0.72 * sc
                pts = np.array([[cx, cy + h], [cx + w, cy], [cx, cy - h], [cx - w, cy]])
                curve = []
                for i in range(4):
                    p0, p1, p2 = pts[i], pts[(i + 1) % 4], pts[(i + 2) % 4]
                    a0 = p0 * 0.2 + p1 * 0.8
                    a1 = p1 * 0.8 + p2 * 0.2
                    for t in np.linspace(0, 1, 6, endpoint=False):
                        curve.append((1 - t) ** 2 * a0 + 2 * (1 - t) * t * p1 + t ** 2 * a1)
                ax.add_patch(Polygon(np.array(curve), closed=True, fill=False,
                                     edgecolor="black", linewidth=1.15 - k * 0.28))
    save(fig, "abstract grid tessellation diamond lattice concentric rounded lozenge pattern black white texture")


if __name__ == "__main__":
    draw()
