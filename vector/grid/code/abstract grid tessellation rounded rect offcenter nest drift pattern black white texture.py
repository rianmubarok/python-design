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
    """Nested rounded squares whose inner rings drift off-center per cell."""
    fig, ax = setup_ax()
    n = 7
    cell = 100 / n
    for r in range(n):
        for c in range(n):
            cx, cy = (c + 0.5) * cell, (r + 0.5) * cell
            rnd0 = 1.0 + 1.4 * (0.5 + 0.5 * np.sin(c * 0.8))
            for k in range(5):
                w = cell * (0.88 - k * 0.14)
                ox = 1.35 * k * np.sin(c * 0.7 + r * 0.4)
                oy = 1.35 * k * np.cos(c * 0.5 - r * 0.6)
                ax.add_patch(FancyBboxPatch((cx - w / 2 + ox, cy - w / 2 + oy), w, w,
                                            boxstyle=f"round,pad=0,rounding_size={max(0.25, rnd0 * (1 - k * 0.12))}",
                                            fill=False, edgecolor="black", linewidth=1.05 - k * 0.14))
    save(fig, "abstract grid tessellation rounded rect offcenter nest drift pattern black white texture")


if __name__ == "__main__":
    draw()
