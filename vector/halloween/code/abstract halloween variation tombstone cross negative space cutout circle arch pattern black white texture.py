import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse, Polygon
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


def draw_tombstone(ax, cx, cy, w, h, fill="black"):
    """Tombstone with:
     - Rounded-arch top (arch rectangle + dome ellipse)
     - Cross-shaped cutout centred in upper body
     - Circle cutout in the arch dome
    The cutouts are rendered in the inverse colour (negative-space carve)."""
    inv = "white" if fill == "black" else "black"

    # === Body: rounded-top rectangle ===
    body_h = h * 0.62
    body_y  = cy - h * 0.50
    ax.add_patch(FancyBboxPatch(
        (cx - w * 0.50, body_y), w, body_h,
        boxstyle=f"round,pad=0,rounding_size={w * 0.06:.4f}",
        facecolor=fill, edgecolor="none", zorder=2))

    # === Arch dome ===
    arch_cy = body_y + body_h
    ax.add_patch(Ellipse(
        (cx, arch_cy), w, h * 0.50,
        facecolor=fill, edgecolor="none", zorder=2))

    # === Negative-space circle in arch ===
    circle_r = w * 0.22
    circle_cy = arch_cy + h * 0.10
    ax.add_patch(Circle((cx, circle_cy), circle_r,
                        facecolor=inv, edgecolor="none", zorder=3))

    # === Cross cutout in body centre ===
    cross_cy  = body_y + body_h * 0.52
    cross_arm_w = w  * 0.14
    cross_arm_h = h  * 0.32
    horiz_w     = w  * 0.36
    horiz_h     = h  * 0.12

    # Vertical bar
    ax.add_patch(FancyBboxPatch(
        (cx - cross_arm_w * 0.5, cross_cy - cross_arm_h * 0.5),
        cross_arm_w, cross_arm_h,
        boxstyle="round,pad=0,rounding_size=0.01",
        facecolor=inv, edgecolor="none", zorder=3))
    # Horizontal bar
    ax.add_patch(FancyBboxPatch(
        (cx - horiz_w * 0.5, cross_cy + cross_arm_h * 0.08),
        horiz_w, horiz_h,
        boxstyle="round,pad=0,rounding_size=0.01",
        facecolor=inv, edgecolor="none", zorder=3))


def draw():
    """Staggered brick-offset grid of tombstones.
    Even columns: black tombstone, white cutouts.
    Odd columns: white tombstone with black outline + black cutouts.
    White background. Seamless."""
    fig, ax = setup_ax()

    cols, rows = 5, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    w = dx * 0.72
    h = dy * 0.82

    for row in range(rows):
        shift = (dx * 0.5) if row % 2 else 0.0
        cy = (row + 0.5) * dy

        for col in range(-1, cols + 2):
            cx = col * dx + shift + dx * 0.5
            fill = "black" if (row + col) % 2 == 0 else "white"

            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    # White tombstones need a thin outline so they read on white bg
                    if fill == "white":
                        ax.add_patch(FancyBboxPatch(
                            (px - w * 0.52, py - h * 0.52),
                            w * 1.04, h * 1.04,
                            boxstyle=f"round,pad=0,rounding_size={w * 0.07:.4f}",
                            facecolor="none", edgecolor="black",
                            linewidth=0.6, zorder=1))
                    draw_tombstone(ax, px, py, w, h, fill=fill)

    save(fig, "abstract halloween variation tombstone cross negative space cutout circle arch pattern black white texture")


if __name__ == "__main__":
    draw()
