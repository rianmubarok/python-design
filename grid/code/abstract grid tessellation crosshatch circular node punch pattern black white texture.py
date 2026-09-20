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
    """Diagonal crosshatch grid punched with concentric circular nodes."""
    fig, ax = setup_ax()
    step = 7.5
    for i in range(-8, 28):
        ax.plot([-10, 110], [i * step - 10, i * step + 110], color="black", linewidth=0.55)
        ax.plot([-10, 110], [i * step + 110, i * step - 10], color="black", linewidth=0.55)
    for row in range(-1, 16):
        for col in range(-1, 16):
            cx, cy = col * step, row * step
            rad = 1.0 + 0.85 * (0.5 + 0.5 * np.sin(col * 0.5) * np.cos(row * 0.4))
            ax.add_patch(Circle((cx, cy), rad, facecolor="white", edgecolor="black", linewidth=0.85, zorder=3))
            ax.add_patch(Circle((cx, cy), rad * 0.45, fill=False, edgecolor="black", linewidth=0.45, zorder=4))
    save(fig, "abstract grid tessellation crosshatch circular node punch pattern black white texture")


if __name__ == "__main__":
    draw()
