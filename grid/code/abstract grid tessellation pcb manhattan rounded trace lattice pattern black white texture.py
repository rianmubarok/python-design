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
    """PCB-like orthogonal traces on a lattice with rounded vias and elbows."""
    fig, ax = setup_ax()
    n = 14
    w = 100 / n
    rng = np.random.default_rng(21)
    for row in range(n):
        for col in range(n):
            x, y = col * w + w / 2, row * w + w / 2
            via = 0.55 + 0.45 * (0.5 + 0.5 * np.sin(col * 0.6 + row * 0.4))
            ax.add_patch(Circle((x, y), via, fill=False, edgecolor="black", linewidth=0.9))
            ax.add_patch(Circle((x, y), via * 0.35, facecolor="black", edgecolor="none"))
            if int(rng.integers(0, 2)):
                ax.plot([x, x + w], [y, y], color="black", linewidth=1.35, solid_capstyle="round")
            else:
                ax.add_patch(Arc((x + w / 2, y + w / 2), w, w, theta1=180, theta2=270,
                                 color="black", linewidth=1.35))
            if int(rng.integers(0, 2)):
                ax.plot([x, x], [y, y + w], color="black", linewidth=1.35, solid_capstyle="round")
    save(fig, "abstract grid tessellation pcb manhattan rounded trace lattice pattern black white texture")


if __name__ == "__main__":
    draw()
