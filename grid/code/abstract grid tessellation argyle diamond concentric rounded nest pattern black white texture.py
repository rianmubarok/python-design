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
    """Argyle diamonds with concentric rounded-diamond nests and a positional drift."""
    fig, ax = setup_ax()
    dw, dh = 11.0, 20.0
    for row in range(10):
        for col in range(14):
            cx = col * dw
            cy = row * dh + (dh / 2 if col % 2 else 0)
            drift = 1.2 * np.sin(row * 0.6) * np.cos(col * 0.5)
            cx += drift
            for k, sc in enumerate((1.0, 0.66, 0.38)):
                w, h = dw * 0.48 * sc, dh * 0.48 * sc
                pts = np.array([[cx, cy + h], [cx + w, cy], [cx, cy - h], [cx - w, cy]])
                curve = []
                n = 4
                for i in range(n):
                    p0, p1, p2 = pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
                    a0 = p0 * 0.18 + p1 * 0.82
                    a1 = p1 * 0.82 + p2 * 0.18
                    for t in np.linspace(0, 1, 7, endpoint=False):
                        curve.append((1 - t) ** 2 * a0 + 2 * (1 - t) * t * p1 + t ** 2 * a1)
                ax.add_patch(Polygon(np.array(curve), closed=True, fill=False,
                                     edgecolor="black", linewidth=1.2 - k * 0.3))
            ax.plot([cx - dw * 0.22, cx + dw * 0.22], [cy - dh * 0.18, cy + dh * 0.18],
                    color="black", linewidth=0.6, linestyle=(0, (2, 2)))
            ax.plot([cx - dw * 0.22, cx + dw * 0.22], [cy + dh * 0.18, cy - dh * 0.18],
                    color="black", linewidth=0.6, linestyle=(0, (2, 2)))
    fit_view(ax)
    save(fig, "abstract grid tessellation argyle diamond concentric rounded nest pattern black white texture")


if __name__ == "__main__":
    draw()
