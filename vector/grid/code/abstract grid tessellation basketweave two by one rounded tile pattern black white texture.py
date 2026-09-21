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
    """Basketweave 2x1 tiles with rounded ends and inner stripe hatch."""
    fig, ax = setup_ax()
    a = 6.8
    for by in range(-1, 10):
        for bx in range(-1, 10):
            ox, oy = bx * 2 * a, by * 2 * a
            rnd = 0.7 + 0.6 * np.sin(bx * 0.7 + by * 0.4)
            # two horizontal then two vertical
            if (bx + by) % 2 == 0:
                tiles = [((ox, oy), 2 * a, a), ((ox, oy + a), 2 * a, a)]
            else:
                tiles = [((ox, oy), a, 2 * a), ((ox + a, oy), a, 2 * a)]
            for (x, y), w, h in tiles:
                ax.add_patch(FancyBboxPatch((x + 0.25, y + 0.25), w - 0.5, h - 0.5,
                                            boxstyle=f"round,pad=0,rounding_size={rnd}",
                                            fill=False, edgecolor="black", linewidth=1.1))
                if w > h:
                    for k in (0.35, 0.5, 0.65):
                        ax.plot([x + 0.9, x + w - 0.9], [y + h * k, y + h * k],
                                color="black", linewidth=0.45)
                else:
                    for k in (0.35, 0.5, 0.65):
                        ax.plot([x + w * k, x + w * k], [y + 0.9, y + h - 0.9],
                                color="black", linewidth=0.45)
    save(fig, "abstract grid tessellation basketweave two by one rounded tile pattern black white texture")


if __name__ == "__main__":
    draw()
