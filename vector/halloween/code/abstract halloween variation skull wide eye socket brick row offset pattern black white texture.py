import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon, Circle
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


def skull(ax, cx, cy, s, fill="black"):
    """Skull with exaggeratedly wide eye sockets — gives a stretched alien look."""
    inv = "white" if fill == "black" else "black"
    edge = "none" if fill == "black" else "black"
    elw = 0.0 if fill == "black" else s * 0.08

    skull_cy = cy + 0.08 * s

    # Cranium — wider than tall
    ax.add_patch(Ellipse((cx, skull_cy + 0.08 * s), 0.82 * s, 0.60 * s,
                         facecolor=fill, edgecolor=edge, linewidth=elw))

    # Jaw
    ax.add_patch(FancyBboxPatch(
        (cx - 0.24 * s, skull_cy - 0.22 * s), 0.48 * s, 0.18 * s,
        boxstyle=f"round,pad=0,rounding_size={0.035*s:.4f}",
        facecolor=fill, edgecolor=edge, linewidth=elw))

    # Extra-wide eye sockets
    for ex in (-0.20 * s, 0.20 * s):
        ax.add_patch(Ellipse((cx + ex, skull_cy + 0.12 * s),
                             0.24 * s, 0.16 * s,
                             facecolor=inv, edgecolor="none"))

    # Nose cavity
    ax.add_patch(Polygon(
        [[cx, skull_cy + 0.02 * s],
         [cx - 0.05 * s, skull_cy - 0.07 * s],
         [cx + 0.05 * s, skull_cy - 0.07 * s]],
        closed=True, facecolor=inv, edgecolor="none"))

    # Teeth — 4 teeth for wide jaw
    for tx in (-0.135 * s, -0.045 * s, 0.045 * s, 0.135 * s):
        ax.add_patch(FancyBboxPatch(
            (cx + tx - 0.018 * s, skull_cy - 0.195 * s),
            0.036 * s, 0.08 * s,
            boxstyle="round,pad=0,rounding_size=0.003",
            facecolor=inv, edgecolor="none"))


def draw():
    """Brick-offset rows of wide-eye-socket skulls. White bg, alternating black/white fills."""
    fig, ax = setup_ax()

    cols, rows = 6, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.72

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            fill = "black" if (row + col) % 2 == 0 else "white"
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    skull(ax, px, py, s, fill=fill)

    save(fig, "abstract halloween variation skull wide eye socket brick row offset pattern black white texture")


if __name__ == "__main__":
    draw()
