import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, FancyBboxPatch
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


def draw_witch_hat(ax, cx, cy, s, fill="black", zorder=2):
    """Simple witch hat: wide brim ellipse + tall cone triangle."""
    # Brim
    ax.add_patch(Ellipse((cx, cy - s * 0.28), s * 1.10, s * 0.22,
                         facecolor=fill, edgecolor="none", zorder=zorder))
    # Cone
    hat_pts = [
        (cx - s * 0.44, cy - s * 0.20),
        (cx + s * 0.44, cy - s * 0.20),
        (cx + s * 0.12, cy + s * 0.72),
        (cx,            cy + s * 0.86),
        (cx - s * 0.12, cy + s * 0.72),
    ]
    ax.add_patch(Polygon(hat_pts, closed=True,
                         facecolor=fill, edgecolor="none", zorder=zorder))
    # Hat band
    band_y = cy - s * 0.02
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.38, band_y - s * 0.06), s * 0.76, s * 0.12,
        boxstyle=f"round,pad=0,rounding_size={s * 0.03:.4f}",
        facecolor="white" if fill == "black" else "black",
        edgecolor="none", zorder=zorder + 1))


def draw():
    """Each tile: a solid black witch hat + its ghost-like 'shadow' offset copy
    rendered in 40% grey (simulating a drop shadow / double-exposure ghost).
    The shadow copy is drawn first (behind), slightly shifted down-right.
    Grid is staggered for seamless tiling. White background."""
    fig, ax = setup_ax()

    cols, rows = 5, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.46

    shadow_dx =  s * 0.22   # shadow offset right
    shadow_dy = -s * 0.18   # shadow offset down

    for row in range(rows):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            cx = col * dx + shift + dx * 0.5
            cy = (row + 0.5) * dy

            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    # Shadow (grey, drawn first at lower zorder)
                    draw_witch_hat(ax, px + shadow_dx, py + shadow_dy,
                                   s, fill="#999999", zorder=2)
                    # Primary hat (solid black on top)
                    draw_witch_hat(ax, px, py, s, fill="black", zorder=4)

    save(fig, "abstract halloween variation witch hat dropped shadow offset double ghost pattern black white texture")


if __name__ == "__main__":
    draw()
