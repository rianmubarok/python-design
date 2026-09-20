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

def draw():
    """Seamless candy-corn triangle tessellation."""
    fig, ax = setup_ax()
    cols, rows = 10, 10
    s = PERIOD / cols
    h = PERIOD / rows
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * s
            cy = (row + 0.5) * h
            up = (row + col) % 2 == 0
            if up:
                tri = np.array([[0, h * 0.42], [-s * 0.42, -h * 0.32], [s * 0.42, -h * 0.32]])
            else:
                tri = np.array([[0, -h * 0.42], [-s * 0.42, h * 0.32], [s * 0.42, h * 0.32]])
            tip = tri[0]
            for ox, oy in WRAPS:
                t = tri + [cx + ox, cy + oy]
                ax.add_patch(Polygon(t, closed=True, fill=False, edgecolor="black", linewidth=1.0))
                tp = tip + [cx + ox, cy + oy]
                for sc in (0.38, 0.68):
                    ax.add_patch(Polygon(tp + (t - tp) * sc, closed=True, fill=False,
                                         edgecolor="black", linewidth=0.5))
    save(fig, "abstract halloween tessellation candy corn triangle tessellation pattern black white texture")


if __name__ == "__main__":
    draw()
