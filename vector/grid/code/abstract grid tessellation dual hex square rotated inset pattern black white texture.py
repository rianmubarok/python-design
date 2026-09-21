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
    """Hex cells with independently rotating rounded-square insets."""
    fig, ax = setup_ax()
    r = 6.0
    dx, dy = r * np.sqrt(3), r * 1.5
    for row in range(-2, 14):
        for col in range(-2, 14):
            cx = col * dx + (dx / 2 if row % 2 else 0)
            cy = row * dy
            ax.add_patch(RegularPolygon((cx, cy), 6, radius=r, orientation=np.pi / 6,
                                        fill=False, edgecolor="black", linewidth=1.1))
            ang = 8 * (col - row) + 10 * np.sin(col * 0.4)
            w = r * (0.95 + 0.12 * np.sin(row * 0.5))
            rnd = 0.4 + 0.7 * (0.5 + 0.5 * np.cos(col * 0.6))
            ax.add_patch(FancyBboxPatch((-w / 2, -w / 2), w, w,
                                        boxstyle=f"round,pad=0,rounding_size={rnd}",
                                        fill=False, edgecolor="black", linewidth=0.75,
                                        transform=Affine2D().rotate_deg(ang).translate(cx, cy) + ax.transData))
    save(fig, "abstract grid tessellation dual hex square rotated inset pattern black white texture")


if __name__ == "__main__":
    draw()
