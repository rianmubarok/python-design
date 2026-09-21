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
    """Classic quarter-circle Truchet with nested radii flipping on a checker."""
    fig, ax = setup_ax()
    cell = 6.4
    rng = np.random.default_rng(3)
    cols = int(120 / cell) + 3
    rows = int(120 / cell) + 3
    for row in range(-2, rows):
        for col in range(-2, cols):
            x, y = col * cell, row * cell
            st = int(rng.integers(0, 2))
            radii = (0.32, 0.62, 0.92) if (row + col) % 2 == 0 else (0.48, 0.88)
            for i, f in enumerate(radii):
                d = cell * f
                lw = 1.35 - i * 0.28
                if st == 0:
                    ax.add_patch(Arc((x, y + cell), d, d, theta1=270, theta2=360, color="black", linewidth=lw))
                    ax.add_patch(Arc((x + cell, y), d, d, theta1=90, theta2=180, color="black", linewidth=lw))
                else:
                    ax.add_patch(Arc((x, y), d, d, theta1=0, theta2=90, color="black", linewidth=lw))
                    ax.add_patch(Arc((x + cell, y + cell), d, d, theta1=180, theta2=270, color="black", linewidth=lw))
    save(fig, "abstract grid tessellation quarter circle truchet nested radius checker pattern black white texture")


if __name__ == "__main__":
    draw()
