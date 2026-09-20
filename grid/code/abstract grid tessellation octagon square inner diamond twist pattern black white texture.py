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
    """Octagon-square tiling with inner diamonds that twist per cell."""
    fig, ax = setup_ax()
    step = 13.2
    for r in range(-1, 10):
        for c in range(-1, 10):
            cx, cy = (c + 0.5) * step, (r + 0.5) * step
            ax.add_patch(RegularPolygon((cx, cy), 8, radius=5.1, orientation=np.pi / 8,
                                        fill=False, edgecolor="black", linewidth=1.15))
            tw = np.deg2rad(12 * np.sin(c * 0.7) + 8 * np.cos(r * 0.5))
            d = 2.4 + 0.6 * np.sin(c + r)
            pts = np.array([[0, d], [d, 0], [0, -d], [-d, 0]])
            ca, sa = np.cos(tw), np.sin(tw)
            rot = pts @ np.array([[ca, sa], [-sa, ca]])
            ax.add_patch(Polygon(rot + [cx, cy], closed=True, fill=False, edgecolor="black", linewidth=0.7))
            sw = 4.2
            ax.add_patch(FancyBboxPatch((cx + step / 2 - sw / 2, cy + step / 2 - sw / 2), sw, sw,
                                        boxstyle="round,pad=0,rounding_size=0.7",
                                        fill=False, edgecolor="black", linewidth=0.85))
    save(fig, "abstract grid tessellation octagon square inner diamond twist pattern black white texture")


if __name__ == "__main__":
    draw()
