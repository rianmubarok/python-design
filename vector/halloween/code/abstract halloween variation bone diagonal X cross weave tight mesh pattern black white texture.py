import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon
from matplotlib.transforms import Affine2D
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


def draw_bone(ax, cx, cy, length, thick, angle, fill="white"):
    """Single bone: shaft + end knobs, rotated by angle around (cx, cy)."""
    tr = Affine2D().rotate_deg_around(cx, cy, np.degrees(angle)) + ax.transData
    half_l = length * 0.5
    shaft_w = thick * 0.28
    knob_r = thick * 0.5

    # Shaft
    ax.add_patch(FancyBboxPatch(
        (cx - half_l, cy - shaft_w),
        length, shaft_w * 2,
        boxstyle=f"round,pad=0,rounding_size={shaft_w*0.8:.4f}",
        facecolor=fill, edgecolor="none",
        transform=tr))

    # End knobs
    for ex in (-half_l, half_l):
        ax.add_patch(Circle((cx + ex, cy), knob_r,
                            facecolor=fill, edgecolor="none",
                            transform=tr))
        # Double knob nub
        ax.add_patch(Circle((cx + ex, cy), knob_r * 0.55,
                            facecolor=fill, edgecolor="none",
                            transform=tr))


def draw():
    """Dense X-cross weave: at every grid intersection, two bones cross at +45° and -45°.
    Tight grid creates a mesh texture. White on black.
    Bones at both diagonals form a woven crosshatch pattern."""
    fig, ax = setup_ax()

    n = 9  # grid density
    dx = PERIOD / n
    bone_length = dx * 1.30    # bones overlap slightly to close gaps
    bone_thick = dx * 0.38

    for row in range(-1, n + 1):
        for col in range(-1, n + 1):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dx
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    draw_bone(ax, px, py, bone_length, bone_thick,
                              angle=np.radians(45), fill="white")
                    draw_bone(ax, px, py, bone_length, bone_thick,
                              angle=np.radians(-45), fill="white")

    save(fig, "abstract halloween variation bone diagonal X cross weave tight mesh pattern black white texture")


if __name__ == "__main__":
    draw()
