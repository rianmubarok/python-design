import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon
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
    ax.set_facecolor("black")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="black")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="black")
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def tombstone_moon(ax, cx, cy, tw, th):
    """Tombstone (white) with full moon disc (white) partially hidden behind it."""
    moon_r = tw * 0.72
    moon_cy = cy - th * 0.18   # moon centres behind upper tombstone
    # draw moon first (behind)
    ax.add_patch(Circle((cx, moon_cy), moon_r, facecolor="white", edgecolor="none", zorder=2))

    # tombstone body (arch top)
    arch_r = tw / 2
    straight_h = th - arch_r
    rect_pts = np.array([
        [cx-tw/2, cy-th/2],
        [cx+tw/2, cy-th/2],
        [cx+tw/2, cy-th/2+straight_h],
        [cx-tw/2, cy-th/2+straight_h],
    ])
    ax.add_patch(Polygon(rect_pts, closed=True, facecolor="white", edgecolor="none", zorder=3))
    theta = np.linspace(0, np.pi, 50)
    arch_pts = np.vstack([
        [cx-arch_r, cy-th/2+straight_h],
        np.column_stack([cx+arch_r*np.cos(theta), cy-th/2+straight_h+arch_r*np.sin(theta)]),
        [cx+arch_r, cy-th/2+straight_h],
    ])
    ax.add_patch(Polygon(arch_pts, closed=True, facecolor="white", edgecolor="none", zorder=3))

    # RIP text simulation — three lines
    line_y = cy - th*0.05
    for i, lw in enumerate([tw*0.5, tw*0.3, tw*0.45]):
        ax.plot([cx-lw/2, cx+lw/2], [line_y-i*th*0.12, line_y-i*th*0.12],
                color="black", linewidth=0.9, zorder=4)
    # crack
    ax.plot([cx+tw*0.12, cx+tw*0.22, cx+tw*0.18],
            [cy+th*0.28, cy+th*0.12, cy-th*0.04],
            color="black", linewidth=0.5, zorder=4)


def draw():
    """5×5 tombstones with full moons rising behind, on black."""
    fig, ax = setup_ax()
    cols, rows = 5, 5
    dx, dy = PERIOD/cols, PERIOD/rows
    tw = dx*0.60
    th = dy*0.80
    for row in range(rows):
        for col in range(cols):
            cx = (col+0.5)*dx + (dx*0.5 if row%2 else 0)
            cy = (row+0.5)*dy
            for ox, oy in WRAPS:
                tombstone_moon(ax, cx+ox, cy+oy, tw, th)
    save(fig, "abstract halloween variation tombstone moon rising behind arch grid pattern black white texture")


if __name__ == "__main__":
    draw()
