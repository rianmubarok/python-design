import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
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
    print(f"Saved: {jpg_path}")


def single_broom(ax, cx, cy, length, angle_deg, fill="black"):
    """One broomstick at angle_deg: handle shaft + bristle fan."""
    a = np.radians(angle_deg)
    shaft_w = length * 0.055
    half = length / 2
    tr = Affine2D().rotate_deg(angle_deg).translate(cx, cy) + ax.transData
    ax.add_patch(FancyBboxPatch((-half, -shaft_w/2), length, shaft_w,
                                boxstyle=f"round,pad=0,rounding_size={shaft_w*0.4:.4f}",
                                facecolor=fill, edgecolor="none", transform=tr))
    bristle_cx = cx + half * np.cos(a)
    bristle_cy = cy + half * np.sin(a)
    bristle_len = length * 0.28
    n_bristles = 9
    spread = np.radians(28)
    for i in range(n_bristles):
        ba = a - spread/2 + spread * i/(n_bristles-1)
        ax.plot([bristle_cx, bristle_cx + bristle_len*np.cos(ba)],
                [bristle_cy, bristle_cy + bristle_len*np.sin(ba)],
                color=fill, linewidth=0.7)
    ax.add_patch(FancyBboxPatch(
        (bristle_cx - shaft_w*1.2, bristle_cy - shaft_w*1.2),
        shaft_w*2.4, shaft_w*2.4,
        boxstyle=f"round,pad=0,rounding_size={shaft_w*0.5:.4f}",
        facecolor=fill, edgecolor="none"))


def draw():
    """Crossed broomstick X pairs — 6×6 grid, alternating black/white backgrounds."""
    fig, ax = setup_ax()
    cols, rows = 6, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    broom_len = min(dx, dy) * 1.10
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            fill = "black" if (row + col) % 2 == 0 else "white"
            bg   = "white" if fill == "black" else "black"
            ax.add_patch(Polygon([[col*dx, row*dy], [(col+1)*dx, row*dy],
                                   [(col+1)*dx, (row+1)*dy], [col*dx, (row+1)*dy]],
                                  closed=True, facecolor=bg, edgecolor="none"))
            for ox, oy in WRAPS:
                single_broom(ax, cx+ox, cy+oy, broom_len,  45, fill)
                single_broom(ax, cx+ox, cy+oy, broom_len, -45, fill)
    save(fig, "abstract halloween variation broomstick crossed X pair tile pattern black white texture")


if __name__ == "__main__":
    draw()
