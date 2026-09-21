import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (
    Arc, Circle, Ellipse, FancyBboxPatch, Polygon, RegularPolygon, Rectangle, PathPatch,
)
from matplotlib.path import Path as MplPath
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


def fit_view(ax, pad=55):
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)


def squircle(cx, cy, rx, ry, p, n=80):
    t = np.linspace(0, 2 * np.pi, n)
    ct, st = np.cos(t), np.sin(t)
    x = cx + rx * np.sign(ct) * (np.abs(ct) ** (2 / p))
    y = cy + ry * np.sign(st) * (np.abs(st) ** (2 / p))
    return x, y

def draw():
    """8-point Islamic stars that alternate rotation and inner radius on a checkerboard."""
    fig, ax = setup_ax()
    scale = 10.5
    for row in range(12):
        for col in range(12):
            cx, cy = col * scale, row * scale
            rot = 22.5 if (row + col) % 2 else 0.0
            r = scale * (0.34 if (row + col) % 2 else 0.42)
            for k, rr in enumerate((r, r * 0.55, r * 0.28)):
                angs = np.deg2rad(np.arange(0, 360, 45) + rot + k * 8)
                ax.add_patch(Polygon(np.column_stack([cx + rr * np.cos(angs), cy + rr * np.sin(angs)]),
                                     closed=True, fill=False, edgecolor="black",
                                     linewidth=1.3 - k * 0.35))
                angs2 = angs + np.deg2rad(22.5)
                ax.add_patch(Polygon(np.column_stack([cx + rr * 0.72 * np.cos(angs2),
                                                      cy + rr * 0.72 * np.sin(angs2)]),
                                     closed=True, fill=False, edgecolor="black",
                                     linewidth=0.7))
    fit_view(ax)
    save(fig, "abstract grid tessellation islamic star checker rotation stagger pattern black white texture")


if __name__ == "__main__":
    draw()
