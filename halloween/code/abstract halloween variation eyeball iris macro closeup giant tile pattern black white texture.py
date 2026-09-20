import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
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
    print(f"Saved: {jpg_path}")


def iris_macro(ax, cx, cy, r, rng):
    """Giant iris closeup filling a tile — radial fiber texture, pupil, highlight."""
    n_fibers = 120
    iris_r = r

    # sclera edge (white ring peeking outside iris)
    ax.add_patch(Circle((cx, cy), iris_r * 1.18, facecolor="white",
                        edgecolor="none", zorder=1))

    # iris base (black)
    ax.add_patch(Circle((cx, cy), iris_r, facecolor="black",
                        edgecolor="none", zorder=2))

    # radial fiber lines — alternating thick/thin, light/mid grey
    for i in range(n_fibers):
        a = 2 * np.pi * i / n_fibers
        inner_r = iris_r * rng.uniform(0.30, 0.45)
        outer_r = iris_r * rng.uniform(0.88, 1.00)
        lw = rng.uniform(0.4, 1.2)
        grey = rng.uniform(0.45, 0.90)
        ax.plot([cx + inner_r * np.cos(a), cx + outer_r * np.cos(a)],
                [cy + inner_r * np.sin(a), cy + outer_r * np.sin(a)],
                color=str(grey), linewidth=lw, alpha=0.7, zorder=3)

    # collarette ring
    for ring_r in (iris_r * 0.42, iris_r * 0.44):
        ax.add_patch(Circle((cx, cy), ring_r, facecolor="none",
                            edgecolor="white", linewidth=0.6, alpha=0.5, zorder=4))

    # limbal ring (dark edge)
    ax.add_patch(Circle((cx, cy), iris_r * 0.97, facecolor="none",
                        edgecolor="black", linewidth=iris_r * 0.06, zorder=5))

    # pupil
    pupil_r = iris_r * 0.36
    ax.add_patch(Circle((cx, cy), pupil_r, facecolor="black",
                        edgecolor="none", zorder=6))

    # highlight 1 (large)
    ax.add_patch(Circle((cx + iris_r * 0.22, cy + iris_r * 0.22),
                        iris_r * 0.14, facecolor="white",
                        edgecolor="none", alpha=0.90, zorder=7))
    # highlight 2 (small)
    ax.add_patch(Circle((cx - iris_r * 0.14, cy + iris_r * 0.30),
                        iris_r * 0.055, facecolor="white",
                        edgecolor="none", alpha=0.75, zorder=7))


def draw():
    """3×3 giant iris tiles — each tile is almost entirely filled by a single macro
    iris closeup. Different pupil orientations per tile."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(88)
    cols, rows = 3, 3
    dx, dy = PERIOD / cols, PERIOD / rows
    r = min(dx, dy) * 0.50
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                iris_macro(ax, cx + ox, cy + oy, r, rng)
    save(fig, "abstract halloween variation eyeball iris macro closeup giant tile pattern black white texture")


if __name__ == "__main__":
    draw()
