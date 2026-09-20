import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon
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


def bat_poly(cx, cy, s):
    pts = np.array([
        [0.00, 0.08],[0.12,0.18],[0.10,0.05],[0.42,0.22],[0.78,0.38],
        [0.62,0.08],[0.95,0.12],[0.55,-0.08],[0.72,-0.28],[0.28,-0.10],
        [0.18,-0.22],[0.08,-0.08],[0.00,-0.18],
        [-0.08,-0.08],[-0.18,-0.22],[-0.28,-0.10],[-0.72,-0.28],
        [-0.55,-0.08],[-0.95,0.12],[-0.62,0.08],[-0.78,0.38],
        [-0.42,0.22],[-0.10,0.05],[-0.12,0.18],
    ]) * s + [cx, cy]
    return pts


def pumpkin_with_bat(ax, cx, cy, s, fill="black", inv="white"):
    # pumpkin body
    for ox_ in (-s*0.24, 0, s*0.24):
        ax.add_patch(Ellipse((cx+ox_, cy), s*0.60, s*0.76, facecolor=fill, edgecolor="none"))
    for ox_ in (-s*0.24, 0, s*0.24):
        ax.plot([cx+ox_,cx+ox_],[cy-s*0.37,cy+s*0.37], color=inv, linewidth=0.7)
    # stem
    stem_top_y = cy + s*0.37 + s*0.18
    ax.add_patch(FancyBboxPatch((cx-s*0.06,cy+s*0.37), s*0.12, s*0.18,
                                boxstyle=f"round,pad=0,rounding_size={s*0.04:.4f}",
                                facecolor=fill, edgecolor="none"))
    # triangle eyes
    for ex in (-s*0.21, s*0.21):
        ax.add_patch(Polygon([[cx+ex,cy+s*0.16],[cx+ex-s*0.10,cy-s*0.02],
                               [cx+ex+s*0.10,cy-s*0.02]], closed=True,
                              facecolor=inv, edgecolor="none"))
    # smile
    mx = np.linspace(cx-s*0.26, cx+s*0.26, 9)
    mpts = [(mx[0], cy-s*0.10)]
    for i,x in enumerate(mx):
        mpts.append((x, cy-s*0.22 if i%2==0 else cy-s*0.10))
    mpts.append((mx[-1], cy-s*0.10))
    ax.add_patch(Polygon(mpts, closed=True, facecolor=inv, edgecolor="none"))
    # small bat perched on stem
    bat_s = s * 0.26
    bat_cx = cx
    bat_cy = stem_top_y + bat_s * 0.12
    ax.add_patch(Polygon(bat_poly(bat_cx, bat_cy, bat_s), closed=True,
                         facecolor=fill, edgecolor="none"))
    for ex in (-0.35*bat_s, 0.35*bat_s):
        ax.add_patch(Circle((bat_cx+ex, bat_cy+0.22*bat_s), 0.09*bat_s,
                            facecolor=inv, edgecolor="none"))


def draw():
    """5×5 pumpkin grid, each with a small bat perched on the stem."""
    fig, ax = setup_ax()
    cols, rows = 5, 5
    dx, dy = PERIOD/cols, PERIOD/rows
    s = min(dx, dy) * 0.76
    for row in range(rows):
        for col in range(cols):
            cx = (col+0.5)*dx + (dx*0.5 if row%2 else 0)
            cy = (row+0.5)*dy - s*0.06
            fill = "black" if (row+col)%2==0 else "white"
            inv = "white" if fill=="black" else "black"
            bg = inv
            ax.add_patch(Polygon([[cx-dx/2,cy-dy/2],[cx+dx/2,cy-dy/2],
                                   [cx+dx/2,cy+dy/2],[cx-dx/2,cy+dy/2]],
                                  closed=True, facecolor=bg, edgecolor="none"))
            for ox, oy in WRAPS:
                pumpkin_with_bat(ax, cx+ox, cy+oy, s, fill, inv)
    save(fig, "abstract halloween variation pumpkin bat perched stem combo pattern black white texture")


if __name__ == "__main__":
    draw()
