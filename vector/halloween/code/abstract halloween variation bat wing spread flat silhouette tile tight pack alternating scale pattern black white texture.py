import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Circle
from matplotlib.path import Path as MPath
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
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def draw_bat(ax, cx, cy, w, h, fill="black"):
    """Flat spread-wing bat silhouette — wide wingspan, no elevation."""
    edge = "none" if fill == "black" else "black"
    elw = 0.0 if fill == "black" else 0.7

    pts = np.array([
        [cx,          cy + h*0.16],   # head top
        [cx + w*0.08, cy + h*0.08],
        [cx + w*0.28, cy + h*0.22],   # outer wing tip upper
        [cx + w*0.50, cy + h*0.06],   # far tip
        [cx + w*0.36, cy - h*0.18],   # wing notch lower
        [cx + w*0.18, cy - h*0.06],
        [cx + w*0.06, cy + h*0.02],
        [cx,          cy - h*0.16],   # body bottom
        [cx - w*0.06, cy + h*0.02],
        [cx - w*0.18, cy - h*0.06],
        [cx - w*0.36, cy - h*0.18],
        [cx - w*0.50, cy + h*0.06],
        [cx - w*0.28, cy + h*0.22],
        [cx - w*0.08, cy + h*0.08],
        [cx,          cy + h*0.16],
    ])
    codes = [MPath.MOVETO] + [MPath.LINETO]*(len(pts)-2) + [MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(pts, codes),
                           facecolor=fill, edgecolor=edge, linewidth=elw, zorder=2))
    ax.add_patch(Circle((cx, cy + h*0.08), w*0.06,
                        facecolor=fill, edgecolor=edge, linewidth=elw, zorder=3))


def draw():
    """5×6 grid. Two alternating scales:
    - Large bat  (s=1.0) at (row+col)%2==0 positions
    - Small bat  (s=0.52) at (row+col)%2==1 positions
    The size contrast creates a dynamic interlocking visual.
    Both black on white background."""
    fig, ax = setup_ax()

    cols, rows = 5, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    w_large = dx * 0.88; h_large = dy * 0.55
    w_small = dx * 0.46; h_small = dy * 0.29

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            large = (row + col) % 2 == 0
            w = w_large if large else w_small
            h = h_large if large else h_small
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    draw_bat(ax, px, py, w, h, fill="black")

    save(fig, "abstract halloween variation bat wing spread flat silhouette tile tight pack alternating scale pattern black white texture")


if __name__ == "__main__":
    draw()
