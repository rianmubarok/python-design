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
    """Greek-key meander on a square grid with rounded turning corners."""
    fig, ax = setup_ax()
    cell = 8.0
    rng = np.random.default_rng(9)
    for row in range(-1, 15):
        for col in range(-1, 15):
            x0, y0 = col * cell, row * cell
            m = cell
            inset = 1.15 + 0.45 * np.sin(col * 0.6)
            # rounded rectangular frame
            ax.add_patch(FancyBboxPatch((x0 + 0.25, y0 + 0.25), m - 0.5, m - 0.5,
                                        boxstyle="round,pad=0,rounding_size=0.7",
                                        fill=False, edgecolor="black", linewidth=0.9))
            # inner meander: spiral-ish rounded path
            rot = int(rng.integers(0, 4)) * 90
            pts = np.array([
                [0.22, 0.22], [0.78, 0.22], [0.78, 0.78], [0.38, 0.78],
                [0.38, 0.42], [0.62, 0.42], [0.62, 0.62], [0.5, 0.62],
            ]) * m
            ca, sa = np.cos(np.deg2rad(rot)), np.sin(np.deg2rad(rot))
            R = np.array([[ca, -sa], [sa, ca]])
            mid = np.array([m / 2, m / 2])
            pts = (pts - mid) @ R.T + mid + [x0, y0]
            ax.plot(pts[:, 0], pts[:, 1], color="black", linewidth=1.35, solid_capstyle="round",
                    solid_joinstyle="round")
    save(fig, "abstract grid tessellation greek key meander rounded corner pattern black white texture")


if __name__ == "__main__":
    draw()
