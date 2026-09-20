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
    """8-point stars with rounded petal overlays and a rotation stagger."""
    fig, ax = setup_ax()
    step = 10.0
    t = np.linspace(0, 2 * np.pi, 64, endpoint=True)
    for row in range(-1, 13):
        for col in range(-1, 13):
            cx, cy = col * step, row * step
            rot = np.deg2rad(22.5 if (row + col) % 2 else 0)
            r = step * 0.38
            angs = np.deg2rad(np.arange(0, 360, 45)) + rot
            ax.add_patch(Polygon(np.column_stack([cx + r * np.cos(angs), cy + r * np.sin(angs)]),
                                 closed=True, fill=False, edgecolor="black", linewidth=1.15))
            ax.add_patch(Polygon(np.column_stack([cx + r * 0.7 * np.cos(angs + np.pi / 8),
                                                  cy + r * 0.7 * np.sin(angs + np.pi / 8)]),
                                 closed=True, fill=False, edgecolor="black", linewidth=0.7))
            # petals
            pr = r * (0.22 + 0.06 * np.sin(col * 0.5))
            for a in angs:
                px = cx + r * 0.92 * np.cos(a)
                py = cy + r * 0.92 * np.sin(a)
                ax.add_patch(Ellipse((px, py), pr * 1.6, pr, angle=np.rad2deg(a),
                                     fill=False, edgecolor="black", linewidth=0.5))
    save(fig, "abstract grid tessellation islamic star rounded petal overlay pattern black white texture")


if __name__ == "__main__":
    draw()
