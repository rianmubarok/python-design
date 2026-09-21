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
    """Argyle diamonds whose height/width ratio stretches in a wave."""
    fig, ax = setup_ax()
    for row in range(-1, 12):
        for col in range(-1, 16):
            dw = 10.5
            dh = 16.0 + 7.0 * np.sin(col * 0.4) * np.cos(row * 0.35)
            cx = col * dw
            cy = row * 18.0 + (9 if col % 2 else 0)
            p = np.array([[cx, cy + dh / 2], [cx + dw / 2, cy], [cx, cy - dh / 2], [cx - dw / 2, cy]])
            style = (row + col) % 3
            if style == 0:
                ax.add_patch(Polygon(p, closed=True, facecolor="black", edgecolor="none"))
            elif style == 1:
                ax.add_patch(Polygon(p, closed=True, facecolor="none", edgecolor="black",
                                     linewidth=1.1, hatch="////"))
            else:
                ax.add_patch(Polygon(p, closed=True, facecolor="white", edgecolor="black", linewidth=0.9))
            ax.plot([cx - dw * 0.28, cx + dw * 0.28], [cy - dh * 0.22, cy + dh * 0.22],
                    color="black", linewidth=0.7, linestyle=(0, (2, 2)))
    save(fig, "abstract grid tessellation argyle diamond aspect stretch wave pattern black white texture")


if __name__ == "__main__":
    draw()
