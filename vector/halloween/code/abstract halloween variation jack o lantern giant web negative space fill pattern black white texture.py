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


def radial_web_bg(ax, cx, cy, r, n_spokes=12, n_rings=10):
    angles = [k*2*np.pi/n_spokes for k in range(n_spokes)]
    for a in angles:
        ax.plot([cx, cx+r*np.cos(a)], [cy, cy+r*np.sin(a)],
                color="white", linewidth=0.5, alpha=0.55)
    for sc in np.linspace(0.12, 1.0, n_rings):
        pts = np.array([[cx+r*sc*np.cos(a), cy+r*sc*np.sin(a)] for a in angles])
        pts = np.vstack([pts, pts[0]])
        ax.plot(pts[:,0], pts[:,1], color="white", linewidth=0.4, alpha=0.55)


def pumpkin(ax, cx, cy, s):
    fill, inv = "white", "black"
    for ox_ in (-s*0.24, 0, s*0.24):
        ax.add_patch(Ellipse((cx+ox_, cy), s*0.60, s*0.76, facecolor=fill, edgecolor="none"))
    for ox_ in (-s*0.24, 0, s*0.24):
        ax.plot([cx+ox_,cx+ox_],[cy-s*0.37,cy+s*0.37], color=inv, linewidth=0.8)
    ax.add_patch(FancyBboxPatch((cx-s*0.06,cy+s*0.37), s*0.12, s*0.18,
                                boxstyle=f"round,pad=0,rounding_size={s*0.04:.4f}",
                                facecolor=fill, edgecolor="none"))
    for ex in (-s*0.21, s*0.21):
        ax.add_patch(Polygon([[cx+ex,cy+s*0.16],[cx+ex-s*0.10,cy-s*0.02],
                               [cx+ex+s*0.10,cy-s*0.02]], closed=True,
                              facecolor=inv, edgecolor="none"))
    mx = np.linspace(cx-s*0.26, cx+s*0.26, 9)
    mpts = [(mx[0],cy-s*0.10)]
    for i,x in enumerate(mx):
        mpts.append((x, cy-s*0.22 if i%2==0 else cy-s*0.10))
    mpts.append((mx[-1],cy-s*0.10))
    ax.add_patch(Polygon(mpts, closed=True, facecolor=inv, edgecolor="none"))


def draw():
    """2×3 tiles — giant single pumpkin per tile on a radial web background."""
    fig, ax = setup_ax()
    cols, rows = 2, 3
    dx, dy = PERIOD/cols, PERIOD/rows
    s = min(dx, dy) * 0.88
    for row in range(rows):
        for col in range(cols):
            cx = (col+0.5)*dx
            cy = (row+0.5)*dy
            for ox, oy in WRAPS:
                radial_web_bg(ax, cx+ox, cy+oy, min(dx,dy)*0.62)
                pumpkin(ax, cx+ox, cy+oy, s)
    save(fig, "abstract halloween variation jack o lantern giant web negative space fill pattern black white texture")


if __name__ == "__main__":
    draw()
