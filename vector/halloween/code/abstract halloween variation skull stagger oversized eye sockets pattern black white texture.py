import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon
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


def skull_big_eyes(ax, cx, cy, s):
    """Skull variant: oversized round eye sockets, staggered placement."""
    # crossbones
    for ang in (35, -35):
        tr = Affine2D().rotate_deg(ang).translate(cx, cy - 0.42 * s) + ax.transData
        ax.add_patch(FancyBboxPatch(
            (-0.62 * s, -0.055 * s), 1.24 * s, 0.11 * s,
            boxstyle=f"round,pad=0,rounding_size={0.05*s:.4f}",
            facecolor="black", edgecolor="none", transform=tr))
        for end in (-0.6 * s, 0.6 * s):
            ax.add_patch(Circle((end, 0), 0.085 * s, facecolor="black",
                                edgecolor="none", transform=tr))
    # cranium
    ax.add_patch(Ellipse((cx, cy + 0.16 * s), 0.82 * s, 0.74 * s,
                         facecolor="black", edgecolor="none"))
    # jaw
    ax.add_patch(FancyBboxPatch(
        (cx - 0.26 * s, cy - 0.24 * s), 0.52 * s, 0.26 * s,
        boxstyle=f"round,pad=0,rounding_size={0.04*s:.4f}",
        facecolor="black", edgecolor="none"))
    # OVERSIZED round eye sockets (larger than original)
    eye_r = 0.185 * s   # original was 0.11 * s wide half
    for sx in (-0.20 * s, 0.20 * s):
        ax.add_patch(Circle((cx + sx, cy + 0.20 * s), eye_r,
                            facecolor="white", edgecolor="none"))
        # tiny pupil dot for eerie look
        ax.add_patch(Circle((cx + sx, cy + 0.20 * s), eye_r * 0.28,
                            facecolor="black", edgecolor="none"))
    # nose triangle
    ax.add_patch(Polygon(
        np.array([[cx, cy + 0.02 * s], [cx - 0.07 * s, cy - 0.08 * s],
                  [cx + 0.07 * s, cy - 0.08 * s]]),
        closed=True, facecolor="white", edgecolor="none"))
    # teeth
    for x in (-0.13 * s, 0.0, 0.13 * s):
        ax.add_patch(FancyBboxPatch(
            (cx + x - 0.028 * s, cy - 0.205 * s), 0.056 * s, 0.115 * s,
            facecolor="white", edgecolor="none"))


def draw():
    """Staggered skull grid with oversized eye sockets — 5 cols wide, offset rows."""
    fig, ax = setup_ax()
    cols, rows = 5, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.76
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                skull_big_eyes(ax, cx + ox, cy + oy, s)
    save(fig, "abstract halloween variation skull stagger oversized eye sockets pattern black white texture")


if __name__ == "__main__":
    draw()
