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

def hat(ax, cx, cy, fill, edge):
    brim = np.array([[cx - 5.4, cy - 1.9], [cx + 5.4, cy - 1.9],
                     [cx + 4.7, cy - 3.15], [cx - 4.7, cy - 3.15]])
    cone = np.array([[cx, cy + 6.4], [cx - 3.15, cy - 1.85], [cx + 3.15, cy - 1.85]])
    ax.add_patch(Polygon(cone, closed=True, facecolor=fill, edgecolor=edge, linewidth=0.85))
    ax.add_patch(Polygon(brim, closed=True, facecolor=fill, edgecolor=edge, linewidth=0.85))
    inv = "white" if fill == "black" else "black"
    ax.add_patch(Polygon(np.array([[cx - 2.75, cy - 0.45], [cx + 2.75, cy - 0.45],
                                   [cx + 2.5, cy - 1.25], [cx - 2.5, cy - 1.25]]),
                         closed=True, facecolor=inv, edgecolor="none"))
    ax.add_patch(FancyBboxPatch((cx - 0.6, cy - 1.35), 1.2, 1.0,
                                boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor=inv, edgecolor="none"))


def draw():
    """Seamless staggered witch-hat tessellation."""
    fig, ax = setup_ax()
    cols, rows = 8, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            fill = "black" if (row + col) % 2 == 0 else "white"
            edge = "none" if fill == "black" else "black"
            for ox, oy in WRAPS:
                hat(ax, cx + ox, cy + oy, fill, edge)
    save(fig, "abstract halloween tessellation witch hat triangle tessellation pattern black white texture")


if __name__ == "__main__":
    draw()
