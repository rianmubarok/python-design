import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
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


def hat(ax, cx, cy, fill, flip=False):
    """Draw a witch hat, optionally flipped upside-down."""
    inv = "white" if fill == "black" else "black"
    edge = "none" if fill == "black" else "black"
    sign = -1 if flip else 1

    # cone (pointing up or down)
    cone = np.array([
        [cx,            cy + sign * 6.4],
        [cx - 3.15,     cy - sign * 1.85],
        [cx + 3.15,     cy - sign * 1.85]
    ])
    # brim
    brim = np.array([
        [cx - 5.4,  cy - sign * 1.9],
        [cx + 5.4,  cy - sign * 1.9],
        [cx + 4.7,  cy - sign * 3.15],
        [cx - 4.7,  cy - sign * 3.15]
    ])
    # band on cone base
    band = np.array([
        [cx - 2.75, cy - sign * 0.45],
        [cx + 2.75, cy - sign * 0.45],
        [cx + 2.5,  cy - sign * 1.25],
        [cx - 2.5,  cy - sign * 1.25]
    ])

    ax.add_patch(Polygon(cone, closed=True, facecolor=fill, edgecolor=edge, linewidth=0.8))
    ax.add_patch(Polygon(brim, closed=True, facecolor=fill, edgecolor=edge, linewidth=0.8))
    ax.add_patch(Polygon(band, closed=True, facecolor=inv, edgecolor="none"))
    ax.add_patch(FancyBboxPatch(
        (cx - 0.6, cy - sign * 1.35 - (0.9 if flip else 0)),
        1.2, 1.0,
        boxstyle="round,pad=0,rounding_size=0.12",
        facecolor=inv, edgecolor="none"))


def draw():
    """Upright and upside-down witch hats interlocked — the downward hat's brim
    slots into the gap above the upward hat's brim, creating a tight zigzag interlock."""
    fig, ax = setup_ax()
    cols, rows = 8, 7
    dx, dy = PERIOD / cols, PERIOD / rows
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            flip = (row + col) % 2 == 1
            fill = "black" if (row + col) % 2 == 0 else "white"
            for ox, oy in WRAPS:
                hat(ax, cx + ox, cy + oy, fill, flip=flip)
    save(fig, "abstract halloween variation witch hat mirrored updown interlock tessellation pattern black white texture")


if __name__ == "__main__":
    draw()
