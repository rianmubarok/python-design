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
    """Escher-style arrows with rounded notches and a scale pulse."""
    fig, ax = setup_ax()
    scale = 8.2
    dx, dy = 0.75 * scale, 0.5 * scale
    for row in range(-12, 36):
        for col in range(-4, 22):
            s = scale * (0.88 + 0.14 * np.sin(col * 0.35) * np.cos(row * 0.22))
            cx, cy = col * dx, row * dy
            notch = 0.18 + 0.08 * np.sin(col + row * 0.3)
            arrow = np.array([
                [-0.5, 0.25], [0.0, 0.25], [0.0, 0.5], [0.5, 0.0],
                [0.0, -0.5], [0.0, -0.25], [-0.5, -0.25], [-notch, 0.0],
            ]) * s
            # round via interpolation
            n = len(arrow)
            curve = []
            for i in range(n):
                p0, p1, p2 = arrow[i], arrow[(i + 1) % n], arrow[(i + 2) % n]
                a0 = p0 * 0.15 + p1 * 0.85
                a1 = p1 * 0.85 + p2 * 0.15
                for t in np.linspace(0, 1, 5, endpoint=False):
                    curve.append((1 - t) ** 2 * a0 + 2 * (1 - t) * t * p1 + t ** 2 * a1)
            fill = "black" if (row + col) % 2 == 0 else "white"
            ax.add_patch(Polygon(np.array(curve) + [cx, cy], closed=True,
                                 facecolor=fill, edgecolor="black", linewidth=0.55))
    save(fig, "abstract grid tessellation interlocking arrow rounded notch scale pulse pattern black white texture")


if __name__ == "__main__":
    draw()
