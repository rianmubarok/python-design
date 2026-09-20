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
    """Rhombitrihexagonal-like nodes: hex, square, triangle with scale stagger."""
    fig, ax = setup_ax()
    s = 6.8
    dx, dy = s * np.sqrt(3), s * 1.5
    for row in range(-2, 14):
        for col in range(-2, 14):
            cx = col * dx + (dx / 2 if row % 2 else 0)
            cy = row * dy
            sc = 0.9 + 0.12 * np.sin(col * 0.45)
            ax.add_patch(RegularPolygon((cx, cy), 6, radius=s * 0.52 * sc, orientation=np.pi / 6,
                                        fill=False, edgecolor="black", linewidth=1.1))
            for k in range(6):
                ang = np.pi / 6 + k * np.pi / 3
                px = cx + s * 0.78 * np.cos(ang)
                py = cy + s * 0.78 * np.sin(ang)
                ax.add_patch(RegularPolygon((px, py), 4, radius=s * 0.22, orientation=ang,
                                            fill=False, edgecolor="black", linewidth=0.7))
    save(fig, "abstract grid tessellation rhombitrihexagonal truncated node pattern black white texture")


if __name__ == "__main__":
    draw()
