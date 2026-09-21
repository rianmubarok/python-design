import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon
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


def pumpkin_face(ax, cx, cy, s, expr=0):
    """
    expr 0 = happy, 1 = angry, 2 = surprised, 3 = evil grin
    White pumpkin on black background.
    """
    fill, inv = "white", "black"
    # body — three lobes
    for ox in (-s * 0.22, 0, s * 0.22):
        ax.add_patch(Ellipse((cx + ox, cy), s * 0.54, s * 0.70,
                             facecolor=fill, edgecolor="none"))
    # ribs
    for ox in (-s * 0.22, 0, s * 0.22):
        ax.plot([cx + ox, cx + ox], [cy - s * 0.33, cy + s * 0.33],
                color=inv, linewidth=0.55, solid_capstyle="round")
    # stem
    ax.add_patch(FancyBboxPatch((cx - s*0.055, cy + s*0.33), s*0.11, s*0.16,
                                boxstyle=f"round,pad=0,rounding_size={s*0.04:.4f}",
                                facecolor=fill, edgecolor="none"))

    if expr == 0:  # happy — simple triangle eyes + wide smile
        for ex in (-s*0.21, s*0.21):
            ax.add_patch(Polygon([[cx+ex, cy+s*0.16],[cx+ex-s*0.10,cy-s*0.02],
                                   [cx+ex+s*0.10,cy-s*0.02]],
                                  closed=True, facecolor=inv, edgecolor="none"))
        mx = np.linspace(cx-s*0.26, cx+s*0.26, 9)
        mpts = [(mx[0], cy-s*0.08)]
        for i,x in enumerate(mx):
            mpts.append((x, cy-s*0.22 if i%2==0 else cy-s*0.08))
        mpts.append((mx[-1], cy-s*0.08))
        ax.add_patch(Polygon(mpts, closed=True, facecolor=inv, edgecolor="none"))

    elif expr == 1:  # angry — slanted eyes + jagged frown
        for side, ex in ((-1,-s*0.21),(1,s*0.21)):
            pts = [[cx+ex+side*s*0.06, cy+s*0.16],
                   [cx+ex-s*0.10, cy+s*0.04],
                   [cx+ex+s*0.10, cy+s*0.04]]
            ax.add_patch(Polygon(pts, closed=True, facecolor=inv, edgecolor="none"))
            # angry brow
            ax.plot([cx+ex-s*0.12, cx+ex+s*0.12],
                    [cy+s*0.22+side*s*0.06, cy+s*0.22-side*s*0.06],
                    color=inv, linewidth=1.0)
        # frown
        mx = np.linspace(cx-s*0.24, cx+s*0.24, 7)
        mpts = [(mx[0], cy-s*0.12)]
        for i,x in enumerate(mx):
            mpts.append((x, cy-s*0.06 if i%2==0 else cy-s*0.18))
        mpts.append((mx[-1], cy-s*0.12))
        ax.add_patch(Polygon(mpts, closed=True, facecolor=inv, edgecolor="none"))

    elif expr == 2:  # surprised — round eyes + O mouth
        for ex in (-s*0.21, s*0.21):
            ax.add_patch(Ellipse((cx+ex, cy+s*0.10), s*0.16, s*0.18,
                                 facecolor=inv, edgecolor="none"))
        ax.add_patch(Ellipse((cx, cy-s*0.16), s*0.18, s*0.22,
                             facecolor=inv, edgecolor="none"))

    else:  # evil grin — slanted diamonds + wide slash
        for ex in (-s*0.21, s*0.21):
            ax.add_patch(Polygon([[cx+ex, cy+s*0.20],[cx+ex-s*0.10,cy+s*0.10],
                                   [cx+ex,cy+s*0.02],[cx+ex+s*0.10,cy+s*0.10]],
                                  closed=True, facecolor=inv, edgecolor="none"))
        # wide horizontal slash
        pts = [(cx-s*0.28, cy-s*0.08),(cx+s*0.28, cy-s*0.08),
               (cx+s*0.26, cy-s*0.20),(cx+s*0.10,cy-s*0.14),
               (cx, cy-s*0.21),(cx-s*0.10,cy-s*0.14),(cx-s*0.26,cy-s*0.20)]
        ax.add_patch(Polygon(pts, closed=True, facecolor=inv, edgecolor="none"))


def draw():
    """Micro-dense 10×12 jack-o-lantern grid, 4 expressions cycling, on black."""
    fig, ax = setup_ax()
    cols, rows = 10, 12
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.74
    exprs = [0, 1, 2, 3]
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            expr = exprs[(row * cols + col) % 4]
            for ox, oy in WRAPS:
                pumpkin_face(ax, cx + ox, cy + oy, s, expr)
    save(fig, "abstract halloween variation jack o lantern micro dense varied expressions pattern black white texture")


if __name__ == "__main__":
    draw()
