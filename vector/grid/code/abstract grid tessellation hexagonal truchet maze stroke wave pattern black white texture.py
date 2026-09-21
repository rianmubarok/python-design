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
    """Hex Truchet maze whose stroke width waves across the field."""
    fig, ax = setup_ax()
    r = 5.6
    dx, dy = r * np.sqrt(3), r * 1.5
    rng = np.random.default_rng(11)
    for row in range(14):
        for col in range(14):
            cx = col * dx + (dx / 2 if row % 2 else 0)
            cy = row * dy
            verts = np.array([
                [cx + r * np.cos(np.pi / 6 + k * np.pi / 3),
                 cy + r * np.sin(np.pi / 6 + k * np.pi / 3)]
                for k in range(6)
            ])
            lw = 0.55 + 1.7 * (0.5 + 0.5 * np.sin(col * 0.45) * np.cos(row * 0.4))
            rot = int(rng.integers(0, 3))
            pairs = [(0, 1, 3, 4), (1, 2, 4, 5), (2, 3, 5, 0)][rot]
            for a, b in ((pairs[0], pairs[1]), (pairs[2], pairs[3])):
                p0, p1 = verts[a], verts[b]
                mx, my = (p0 + p1) / 2
                # bulge toward cell center
                qx, qy = (mx + cx) / 2, (my + cy) / 2
                t = np.linspace(0, 1, 18)
                xs = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * qx + t ** 2 * p1[0]
                ys = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * qy + t ** 2 * p1[1]
                ax.plot(xs, ys, color="black", linewidth=lw, solid_capstyle="round")
    fit_view(ax)
    save(fig, "abstract grid tessellation hexagonal truchet maze stroke wave pattern black white texture")


if __name__ == "__main__":
    draw()
