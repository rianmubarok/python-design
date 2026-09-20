import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (
    Arc, Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle,
)
from matplotlib.transforms import Affine2D
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
EPS_DIR = OUTPUT_DIR / \"eps\"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_clip_on(True)
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    eps_path = EPS_DIR / f\"{name} {DATE}.eps\"
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format=\"eps\", pad_inches=0, facecolor=\"white\", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")

def pentagram(cx, cy, r):
    angs = -np.pi / 2 + np.arange(5) * 2 * np.pi / 5
    verts = np.column_stack([cx + r * np.cos(angs), cy + r * np.sin(angs)])
    return verts[[0, 2, 4, 1, 3, 0]]


def draw():
    """Seamless pentacle lattice."""
    fig, ax = setup_ax()
    n = 8
    step = PERIOD / n
    r = step * 0.38
    for row in range(n):
        for col in range(n):
            cx = (col + 0.5) * step
            cy = (row + 0.5) * step
            for ox, oy in WRAPS:
                x, y = cx + ox, cy + oy
                ax.add_patch(Circle((x, y), r, fill=False, edgecolor="black", linewidth=1.25))
                ax.add_patch(Circle((x, y), r * 0.82, fill=False, edgecolor="black", linewidth=0.45))
                star = pentagram(x, y, r * 0.78)
                ax.plot(star[:, 0], star[:, 1], color="black", linewidth=0.95)
                ax.add_patch(Circle((x, y), 0.28, facecolor="black", edgecolor="none"))
    save(fig, "abstract halloween tessellation pentacle circle grid pattern black white texture")


if __name__ == "__main__":
    draw()
