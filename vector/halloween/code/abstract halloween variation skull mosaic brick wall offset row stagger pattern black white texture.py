import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon, Rectangle
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


def draw_skull(ax, cx, cy, s, fill="white"):
    """Compact skull silhouette sized to fit a brick-cell."""
    inv = "black" if fill == "white" else "white"
    edge = "black" if fill == "white" else "none"
    elw = 0.5 if fill == "white" else 0.0

    skull_cy = cy + 0.06 * s

    # Cranium
    ax.add_patch(Ellipse((cx, skull_cy + 0.09 * s), 0.72 * s, 0.62 * s,
                         facecolor=fill, edgecolor=edge, linewidth=elw, zorder=2))
    # Jaw — no edge: sits inside the body, outline would bleed at the join seam
    ax.add_patch(FancyBboxPatch(
        (cx - 0.22 * s, skull_cy - 0.20 * s), 0.44 * s, 0.18 * s,
        boxstyle=f"round,pad=0,rounding_size={0.035 * s:.4f}",
        facecolor=fill, edgecolor="none", linewidth=0, zorder=2))

    # Eyes
    eye_y = skull_cy + 0.13 * s
    for ex in (-0.155 * s, 0.155 * s):
        ax.add_patch(Ellipse((cx + ex, eye_y), 0.16 * s, 0.17 * s,
                             facecolor=inv, edgecolor="none", zorder=3))

    # Nose
    ax.add_patch(Polygon(
        [[cx, skull_cy + 0.00 * s],
         [cx - 0.05 * s, skull_cy - 0.07 * s],
         [cx + 0.05 * s, skull_cy - 0.07 * s]],
        closed=True, facecolor=inv, edgecolor="none", zorder=3))

    # Three teeth
    for tx in (-0.09 * s, 0.0, 0.09 * s):
        ax.add_patch(FancyBboxPatch(
            (cx + tx - 0.02 * s, skull_cy - 0.175 * s),
            0.04 * s, 0.085 * s,
            boxstyle="round,pad=0,rounding_size=0.003",
            facecolor=inv, edgecolor="none", zorder=3))


def draw():
    """Brick-wall offset mosaic: each brick cell contains one skull.
    Brick colours alternate black/white in a checkerboard per brick,
    with thin mortar lines separating cells.
    Odd rows are offset by half a brick width — classic brick-bond layout."""
    fig, ax = setup_ax()

    cols = 8
    rows = 10
    brick_w = PERIOD / cols
    brick_h = PERIOD / rows
    mortar = 0.5            # gap width in units
    s = min(brick_w, brick_h) * 0.50

    for row in range(-1, rows + 2):
        shift = (brick_w * 0.5) if (row % 2 != 0) else 0.0
        for col in range(-1, cols + 2):
            cx = col * brick_w + shift + brick_w * 0.5
            cy = row * brick_h + brick_h * 0.5

            fill = "white" if (row + col) % 2 == 0 else "black"
            bg_fill = "black" if fill == "white" else "white"

            for ox, oy in WRAPS:
                bx, by = cx + ox, cy + oy
                if -brick_w <= bx <= PERIOD + brick_w and -brick_h <= by <= PERIOD + brick_h:
                    # Brick cell rectangle
                    ax.add_patch(Rectangle(
                        (bx - brick_w * 0.5 + mortar * 0.5,
                         by - brick_h * 0.5 + mortar * 0.5),
                        brick_w - mortar, brick_h - mortar,
                        facecolor=bg_fill, edgecolor="none", zorder=1))
                    draw_skull(ax, bx, by, s, fill=fill)

    save(fig, "abstract halloween variation skull mosaic brick wall offset row stagger pattern black white texture")


if __name__ == "__main__":
    draw()
