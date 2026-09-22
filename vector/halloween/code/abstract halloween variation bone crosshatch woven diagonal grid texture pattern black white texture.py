import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse
from matplotlib.transforms import Affine2D
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI  = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR  = SCRIPT_DIR.parent / "output"
JPG_DIR     = OUTPUT_DIR / "jpg"
SVG_DIR     = OUTPUT_DIR / "svg"
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


def bone(ax, cx, cy, length, angle_deg, fill="white"):
    """Single bone shape: shaft + knob ends, centred at (cx, cy), rotated."""
    a = np.radians(angle_deg)
    tr = Affine2D().rotate(a).translate(cx, cy) + ax.transData
    shaft_w = length * 0.090
    shaft_l = length * 0.80
    knob_r  = length * 0.130

    # shaft
    ax.add_patch(FancyBboxPatch(
        (-shaft_l * 0.5, -shaft_w * 0.5), shaft_l, shaft_w,
        boxstyle=f"round,pad=0,rounding_size={shaft_w*0.40:.4f}",
        facecolor=fill, edgecolor="none", transform=tr))

    # end knobs (two circles per end, offset perpendicularly)
    for sign_x in (-1, 1):
        kx = sign_x * shaft_l * 0.50
        for sign_y in (-1, 1):
            ky = sign_y * knob_r * 0.45
            ax.add_patch(Circle((kx, ky), knob_r * 0.75,
                                facecolor=fill, edgecolor="none", transform=tr))


def draw():
    """Dense crosshatch weave of bones at ±45°.
    Every grid cell has one bone at +45° and one at -45°, creating an interlocked X grid.
    A secondary offset grid adds bones at the intersection points for maximum weave density.
    White bones on black background.
    """
    fig, ax = setup_ax()
    cols, rows = 6, 6
    dx = PERIOD / cols
    dy = PERIOD / rows
    bone_len = min(dx, dy) * 1.15

    # Primary grid: +45 and -45 at every node
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                bone(ax, cx + ox, cy + oy, bone_len, +45, fill="white")
                bone(ax, cx + ox, cy + oy, bone_len, -45, fill="white")

    # Secondary grid offset by half step: fills gaps at intersections
    for row in range(rows):
        for col in range(cols):
            cx = (col + 1.0) * dx
            cy = (row + 1.0) * dy
            for ox, oy in WRAPS:
                bone(ax, cx + ox, cy + oy, bone_len * 0.70, +45, fill="white")
                bone(ax, cx + ox, cy + oy, bone_len * 0.70, -45, fill="white")

    save(fig,
         "abstract halloween variation bone crosshatch woven diagonal grid "
         "texture pattern black white texture")


if __name__ == "__main__":
    draw()
