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
    print(f"Saved: {jpg_path} | {svg_path}")


def hat(ax, cx, cy, fill, scale=1.0):
    inv = "white" if fill=="black" else "black"
    edge = "none" if fill=="black" else "black"
    s = scale
    cone = np.array([[cx, cy+6.4*s],[cx-3.15*s, cy-1.85*s],[cx+3.15*s, cy-1.85*s]])
    brim = np.array([[cx-5.4*s,cy-1.9*s],[cx+5.4*s,cy-1.9*s],
                     [cx+4.7*s,cy-3.15*s],[cx-4.7*s,cy-3.15*s]])
    band = np.array([[cx-2.75*s,cy-0.45*s],[cx+2.75*s,cy-0.45*s],
                     [cx+2.5*s,cy-1.25*s],[cx-2.5*s,cy-1.25*s]])
    ax.add_patch(Polygon(cone, closed=True, facecolor=fill, edgecolor=edge, linewidth=0.7))
    ax.add_patch(Polygon(brim, closed=True, facecolor=fill, edgecolor=edge, linewidth=0.7))
    ax.add_patch(Polygon(band, closed=True, facecolor=inv, edgecolor="none"))
    ax.add_patch(FancyBboxPatch((cx-0.6*s,cy-1.35*s),1.2*s,1.0*s,
                                boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor=inv, edgecolor="none"))


def broom(ax, cx, cy, length, angle_deg, fill):
    a = np.radians(angle_deg)
    sw = length*0.055; half = length/2
    tr = Affine2D().rotate_deg(angle_deg).translate(cx,cy)+ax.transData
    ax.add_patch(FancyBboxPatch((-half,-sw/2), length, sw,
                                boxstyle=f"round,pad=0,rounding_size={sw*0.4:.4f}",
                                facecolor=fill, edgecolor="none", transform=tr))
    bx = cx+half*np.cos(a); by = cy+half*np.sin(a)
    blen = length*0.28; n=9; spread=np.radians(28)
    for i in range(n):
        ba = a-spread/2+spread*i/(n-1)
        ax.plot([bx,bx+blen*np.cos(ba)],[by,by+blen*np.sin(ba)],
                color=fill, linewidth=0.7)


def draw():
    """Diagonal stripe alternation: hat rows and broom rows alternate.
    Hat stripes go NW→SE, broom stripes go NE→SW."""
    fig, ax = setup_ax()
    cols, rows = 7, 7
    dx, dy = PERIOD/cols, PERIOD/rows
    blen = min(dx,dy)*1.05
    for row in range(rows):
        for col in range(cols):
            cx = (col+0.5)*dx+(dx*0.5 if row%2 else 0)
            cy = (row+0.5)*dy
            use_hat = (row+col) % 2 == 0
            fill = "black" if (row+col)//2 % 2 == 0 else "white"
            bg = "white" if fill=="black" else "black"
            ax.add_patch(Polygon([[cx-dx/2,cy-dy/2],[cx+dx/2,cy-dy/2],
                                   [cx+dx/2,cy+dy/2],[cx-dx/2,cy+dy/2]],
                                  closed=True, facecolor=bg, edgecolor="none"))
            for ox, oy in WRAPS:
                if use_hat:
                    hat(ax, cx+ox, cy+oy, fill, scale=dx/13.0)
                else:
                    broom(ax, cx+ox, cy+oy, blen, 35 if col%2==0 else -35, fill)
    save(fig, "abstract halloween variation witch hat broomstick diagonal stripe alternation pattern black white texture")


if __name__ == "__main__":
    draw()
