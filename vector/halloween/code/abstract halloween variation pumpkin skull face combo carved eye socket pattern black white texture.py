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


def draw_pumpskull(ax, cx, cy, s, fill="white"):
    """Hybrid: pumpkin body + skull-style oval eye sockets + nose cavity + skull teeth.
    The pumpkin lobes form the cranium; skull features are carved in."""
    inv = "black" if fill == "white" else "white"

    # Pumpkin body — three lobes merged into cranium shape
    for ddx in (-s*0.20, 0.0, s*0.20):
        ax.add_patch(Ellipse((cx + ddx, cy + s*0.02), s*0.30, s*0.52,
                             facecolor=fill, edgecolor="none", zorder=2))
    # Stem
    ax.add_patch(FancyBboxPatch(
        (cx - s*0.04, cy + s*0.26), s*0.08, s*0.12,
        boxstyle=f"round,pad=0,rounding_size={s*0.015:.4f}",
        facecolor=fill, edgecolor="none", zorder=2))

    # Skull-style OVAL eye sockets (larger, rounder than triangle)
    for ex in (-s*0.155, s*0.155):
        ax.add_patch(Ellipse((cx + ex, cy + s*0.14),
                             s*0.16, s*0.19,
                             facecolor=inv, edgecolor="none", zorder=3))

    # Skull nose cavity (inverted triangle)
    ax.add_patch(Polygon(
        [[cx,          cy + s*0.02],
         [cx - s*0.055, cy - s*0.08],
         [cx + s*0.055, cy - s*0.08]],
        closed=True, facecolor=inv, edgecolor="none", zorder=3))

    # Skull-style teeth (3 rectangular)
    for tx in (-s*0.10, 0.0, s*0.10):
        ax.add_patch(FancyBboxPatch(
            (cx + tx - s*0.024, cy - s*0.20),
            s*0.048, s*0.09,
            boxstyle="round,pad=0,rounding_size=0.003",
            facecolor=inv, edgecolor="none", zorder=3))


def draw():
    """4×5 hex-packed grid of pumpskull hybrids. White on black.
    Alternating rows offset by half cell for hex packing."""
    fig, ax = setup_ax()

    cols, rows = 4, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.74

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    draw_pumpskull(ax, px, py, s, fill="white")

    save(fig, "abstract halloween variation pumpkin skull face combo carved eye socket pattern black white texture")


if __name__ == "__main__":
    draw()
