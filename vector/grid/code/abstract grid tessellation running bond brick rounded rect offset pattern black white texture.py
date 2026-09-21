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
    """Running-bond brick grid of rounded rectangles with waving corner radii."""
    fig, ax = setup_ax()
    bw, bh = 14.0, 6.4
    for row in range(-2, 20):
        for col in range(-2, 12):
            ox = (bw / 2) if row % 2 else 0
            cx = col * bw + ox
            cy = row * bh
            rnd = 0.35 + 1.35 * (0.5 + 0.5 * np.sin(col * 0.55) * np.cos(row * 0.4))
            ax.add_patch(FancyBboxPatch((cx + 0.35, cy + 0.35), bw - 0.7, bh - 0.7,
                                        boxstyle=f"round,pad=0,rounding_size={rnd}",
                                        fill=False, edgecolor="black", linewidth=1.15))
            ax.add_patch(FancyBboxPatch((cx + 1.6, cy + 1.45), bw - 3.2, bh - 2.9,
                                        boxstyle=f"round,pad=0,rounding_size={rnd * 0.55}",
                                        fill=False, edgecolor="black", linewidth=0.5))
    save(fig, "abstract grid tessellation running bond brick rounded rect offset pattern black white texture")


if __name__ == "__main__":
    draw()
