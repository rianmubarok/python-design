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
    """Kagome dual-triangle lattice with pinched, scaling node rings."""
    fig, ax = setup_ax()
    scale = 7.2
    h = scale * np.sqrt(3) / 2
    for row in range(16):
        for col in range(16):
            cx = col * scale * 1.5
            cy = row * h * 2
            if col % 2:
                cy += h
            pinch = 0.72 + 0.28 * np.sin(col * 0.5) * np.cos(row * 0.45)
            r = scale * 0.78 * pinch
            for sign, off in ((1, 90), (-1, 270)):
                angs = np.deg2rad(np.array([off, off + 120, off + 240]))
                ax.add_patch(Polygon(np.column_stack([cx + r * np.cos(angs), cy + r * np.sin(angs)]),
                                     closed=True, fill=False, edgecolor="black", linewidth=1.35))
            nr = 0.7 + 1.35 * (0.5 + 0.5 * np.sin((cx + cy) * 0.08))
            ax.add_patch(Circle((cx, cy), nr, fill=False, edgecolor="black", linewidth=0.7))
            ax.add_patch(Circle((cx, cy), nr * 0.45, fill=False, edgecolor="black", linewidth=0.4))
    fit_view(ax)
    save(fig, "abstract grid tessellation kagome lattice node pinch scale pattern black white texture")


if __name__ == "__main__":
    draw()
