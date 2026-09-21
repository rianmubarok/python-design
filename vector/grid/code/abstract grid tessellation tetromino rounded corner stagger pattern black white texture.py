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
    """Interlocking tetrominoes with rounded corners and staggered fill."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(5)
    gs = 24
    cs = 100 / gs
    occupied = np.zeros((gs, gs), dtype=bool)
    shapes = [
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (2, 0), (1, 1)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 1), (1, 1), (1, 0), (2, 0)],
    ]
    tiles = []
    for _ in range(900):
        shape = shapes[int(rng.integers(0, len(shapes)))]
        rot = int(rng.integers(0, 4))
        r0, c0 = int(rng.integers(0, gs)), int(rng.integers(0, gs))
        coords = []
        ok = True
        for dr, dc in shape:
            if rot == 1:
                dr, dc = -dc, dr
            elif rot == 2:
                dr, dc = -dr, -dc
            elif rot == 3:
                dr, dc = dc, -dr
            rr, cc = r0 + dr, c0 + dc
            if not (0 <= rr < gs and 0 <= cc < gs) or occupied[rr, cc]:
                ok = False
                break
            coords.append((rr, cc))
        if not ok:
            continue
        for rr, cc in coords:
            occupied[rr, cc] = True
        tiles.append(coords)
    for i, coords in enumerate(tiles):
        rnd = 0.35 + 0.55 * ((i % 5) / 4)
        fill = "black" if i % 2 == 0 else "white"
        for rr, cc in coords:
            ax.add_patch(FancyBboxPatch((cc * cs + 0.18, rr * cs + 0.18), cs - 0.36, cs - 0.36,
                                        boxstyle=f"round,pad=0,rounding_size={rnd}",
                                        facecolor=fill, edgecolor="black", linewidth=0.7))
    save(fig, "abstract grid tessellation tetromino rounded corner stagger pattern black white texture")


if __name__ == "__main__":
    draw()
