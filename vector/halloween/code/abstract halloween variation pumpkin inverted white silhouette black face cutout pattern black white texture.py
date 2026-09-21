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


def pumpkin_inverted(ax, cx, cy, s):
    """White pumpkin on black, features cut OUT as black (negative space)."""
    # white body
    for ox_ in (-s*0.24, 0, s*0.24):
        ax.add_patch(Ellipse((cx+ox_, cy), s*0.60, s*0.76,
                             facecolor="white", edgecolor="none"))
    # ribs (black lines on white)
    for ox_ in (-s*0.24, 0, s*0.24):
        ax.plot([cx+ox_,cx+ox_],[cy-s*0.37,cy+s*0.37],
                color="black", linewidth=0.7)
    # stem white
    ax.add_patch(FancyBboxPatch((cx-s*0.06,cy+s*0.37),s*0.12,s*0.18,
                                boxstyle=f"round,pad=0,rounding_size={s*0.04:.4f}",
                                facecolor="white", edgecolor="none"))
    # eyes cut out as BLACK triangles
    for ex in (-s*0.21, s*0.21):
        ax.add_patch(Polygon([[cx+ex,cy+s*0.16],[cx+ex-s*0.10,cy-s*0.02],
                               [cx+ex+s*0.10,cy-s*0.02]],
                              closed=True, facecolor="black", edgecolor="none"))
    # mouth cut out as BLACK jagged
    mx = np.linspace(cx-s*0.26, cx+s*0.26, 9)
    mpts = [(mx[0],cy-s*0.10)]
    for i,x in enumerate(mx):
        mpts.append((x, cy-s*0.22 if i%2==0 else cy-s*0.10))
    mpts.append((mx[-1],cy-s*0.10))
    ax.add_patch(Polygon(mpts, closed=True, facecolor="black", edgecolor="none"))


def draw():
    """4×5 inverted pumpkins — white body on black, face features cut as black voids."""
    fig, ax = setup_ax()
    cols, rows = 4, 5
    dx, dy = PERIOD/cols, PERIOD/rows
    s = min(dx,dy)*0.82
    for row in range(rows):
        for col in range(cols):
            cx = (col+0.5)*dx+(dx*0.5 if row%2 else 0)
            cy = (row+0.5)*dy
            for ox, oy in WRAPS:
                pumpkin_inverted(ax, cx+ox, cy+oy, s)
    save(fig, "abstract halloween variation pumpkin inverted white silhouette black face cutout pattern black white texture")


if __name__ == "__main__":
    draw()
