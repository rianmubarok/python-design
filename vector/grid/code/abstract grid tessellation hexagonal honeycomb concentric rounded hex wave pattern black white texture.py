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
    """Honeycomb with concentric inner hexes whose scale and rounding pulse."""
    fig, ax = setup_ax()
    r0 = 5.0
    dx, dy = r0 * np.sqrt(3), r0 * 1.5
    t = np.linspace(0, 2 * np.pi, 48)
    for row in range(-2, 16):
        for col in range(-2, 16):
            cx = col * dx + (dx / 2 if row % 2 else 0)
            cy = row * dy
            pulse = 0.82 + 0.18 * np.sin(col * 0.45) * np.cos(row * 0.4)
            for k, sc in enumerate((1.0, 0.68, 0.38)):
                rr = r0 * pulse * sc
                p = 8.0 - 4.5 * k / 2 + 1.2 * np.sin(col + row)
                xs = cx + rr * np.sign(np.cos(t)) * (np.abs(np.cos(t)) ** (2 / p))
                ys = cy + rr * np.sign(np.sin(t)) * (np.abs(np.sin(t)) ** (2 / p))
                # mix hex-ish by sampling 6-fold
                angs = t + np.pi / 6
                mix = 0.35 + 0.2 * k
                hx = cx + rr * np.cos(angs) * (1 + 0.12 * np.cos(6 * angs))
                hy = cy + rr * np.sin(angs) * (1 + 0.12 * np.cos(6 * angs))
                ax.plot(xs * (1 - mix) + hx * mix, ys * (1 - mix) + hy * mix,
                        color="black", linewidth=1.15 - k * 0.28)
    save(fig, "abstract grid tessellation hexagonal honeycomb concentric rounded hex wave pattern black white texture")


if __name__ == "__main__":
    draw()
