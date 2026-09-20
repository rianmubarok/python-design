import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch
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
    print(f"Saved: {jpg_path}")


def single_bone(ax, cx, cy, length, width, angle_deg, fill="white"):
    """One bone — shaft + two end knobs."""
    tr = Affine2D().rotate_deg(angle_deg).translate(cx, cy) + ax.transData
    half = length / 2
    knob_r = width * 0.72
    # shaft
    ax.add_patch(FancyBboxPatch(
        (-half, -width/2), length, width,
        boxstyle=f"round,pad=0,rounding_size={width*0.4:.4f}",
        facecolor=fill, edgecolor="none", transform=tr))
    # end knobs
    for ex in (-half, half):
        ax.add_patch(Circle((ex, 0), knob_r, facecolor=fill,
                            edgecolor="none", transform=tr))
        # small secondary knob
        for off in (-knob_r * 0.55, knob_r * 0.55):
            ax.add_patch(Circle((ex, off), knob_r * 0.45, facecolor=fill,
                                edgecolor="none", transform=tr))


def bone_pile(ax, cx, cy, pile_r, n_bones, rng):
    """Randomly scattered bone pile centred at (cx, cy)."""
    for _ in range(n_bones):
        dist = rng.uniform(0, pile_r * 0.80)
        ang = rng.uniform(0, 2 * np.pi)
        bx = cx + dist * np.cos(ang)
        by = cy + dist * np.sin(ang)
        blen = rng.uniform(pile_r * 0.45, pile_r * 0.85)
        bwidth = blen * rng.uniform(0.08, 0.13)
        bangle = rng.uniform(0, 180)
        single_bone(ax, bx, by, blen, bwidth, bangle)


def draw():
    """Seamless scattered bone pile field — 6×6 heap nodes on black."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(22)
    cols, rows = 6, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    pile_r = min(dx, dy) * 0.50
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + rng.uniform(-dx*0.08, dx*0.08)
            cy = (row + 0.5) * dy + rng.uniform(-dy*0.08, dy*0.08)
            n = rng.integers(5, 9)
            for ox, oy in WRAPS:
                bone_pile(ax, cx + ox, cy + oy, pile_r, n, rng)
    save(fig, "abstract halloween variation bone pile heap scattered organic pattern black white texture")


if __name__ == "__main__":
    draw()
