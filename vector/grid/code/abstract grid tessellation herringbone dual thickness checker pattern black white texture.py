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
    """Herringbone weave with checkerboard dual stroke thickness."""
    fig, ax = setup_ax()
    length, width = 12.8, 3.0
    step = 7.6
    for row in range(-4, 22):
        for col in range(-4, 22):
            cx = col * step * 0.7
            cy = row * step * 0.7 + (step * 0.35 if col % 2 else 0)
            ang = 45 if col % 2 == 0 else -45
            lw = 1.35 if (row + col) % 2 == 0 else 0.55
            rnd = 0.55 if (row + col) % 2 == 0 else 1.15
            ax.add_patch(FancyBboxPatch((-length / 2, -width / 2), length, width,
                                        boxstyle=f"round,pad=0,rounding_size={rnd}",
                                        fill=False, edgecolor="black", linewidth=lw,
                                        transform=Affine2D().rotate_deg(ang).translate(cx, cy) + ax.transData))
    save(fig, "abstract grid tessellation herringbone dual thickness checker pattern black white texture")


if __name__ == "__main__":
    draw()
