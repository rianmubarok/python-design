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


def draw_bottle(ax, cx, cy, s, fill="black"):
    """Potion bottle silhouette: round body + neck + stopper."""
    inv = "white" if fill == "black" else "black"
    edge = "none" if fill == "black" else "black"
    elw = 0.0 if fill == "black" else 0.7
    body_r = s * 0.32

    # Body
    ax.add_patch(Circle((cx, cy - s * 0.07), body_r,
                        facecolor=fill, edgecolor=edge, linewidth=elw))
    # Neck
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.075, cy + s * 0.20), s * 0.15, s * 0.20,
        boxstyle="square,pad=0",
        facecolor=fill, edgecolor=edge, linewidth=elw))
    # Stopper
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.095, cy + s * 0.38), s * 0.19, s * 0.075,
        boxstyle=f"round,pad=0,rounding_size={s*0.02:.4f}",
        facecolor=fill, edgecolor=edge, linewidth=elw))
    # Label rectangle
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.155, cy - s * 0.19), s * 0.31, s * 0.18,
        boxstyle=f"round,pad=0,rounding_size={s*0.018:.4f}",
        facecolor=inv, edgecolor="none"))
    # Skull symbol — simplified dots + head circle
    skull_r = s * 0.042
    ax.add_patch(Circle((cx, cy - s * 0.08), skull_r, facecolor=fill, edgecolor="none"))
    for dx2 in (-skull_r*0.42, skull_r*0.42):
        ax.add_patch(Circle((cx + dx2, cy - s * 0.08), skull_r * 0.28,
                            facecolor=inv, edgecolor="none"))
    # Bubbles (outline circles in body)
    for bx, by, br in [(-0.11, 0.02, 0.032), (0.09, 0.09, 0.026)]:
        ax.add_patch(Circle((cx + bx*s, cy + by*s), br*s,
                            facecolor="none", edgecolor=inv, linewidth=0.6))


def draw():
    """5×6 grid of potion bottles. Diagonal stripe fill:
    (col − row) % 2 == 0 → black bottle, else white bottle.
    White background. Creates alternating diagonal diagonal stripe rhythm."""
    fig, ax = setup_ax()

    cols, rows = 5, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.72

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            fill = "black" if (col - row) % 2 == 0 else "white"
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -12 <= px <= PERIOD + 12 and -12 <= py <= PERIOD + 12:
                    draw_bottle(ax, px, py, s, fill=fill)

    save(fig, "abstract halloween variation potion bottle diagonal stripe alternating silhouette fill pattern black white texture")


if __name__ == "__main__":
    draw()
