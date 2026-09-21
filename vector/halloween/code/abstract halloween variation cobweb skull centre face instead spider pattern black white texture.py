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


def web_skull(ax, cx, cy, r):
    spokes = 8
    angles = [k*np.pi/4 for k in range(spokes)]
    for a in angles:
        ax.plot([cx, cx+r*np.cos(a)], [cy, cy+r*np.sin(a)],
                color="white", linewidth=0.7)
    for sc in (0.28, 0.50, 0.72, 0.96):
        pts = np.array([[cx+r*sc*np.cos(a), cy+r*sc*np.sin(a)] for a in angles])
        pts = np.vstack([pts, pts[0]])
        ax.plot(pts[:,0], pts[:,1], color="white", linewidth=0.55)

    # skull at centre
    s = r * 0.32
    # cranium
    ax.add_patch(Ellipse((cx, cy+0.16*s), 0.82*s, 0.74*s, facecolor="white", edgecolor="none"))
    ax.add_patch(FancyBboxPatch((cx-0.26*s, cy-0.24*s), 0.52*s, 0.26*s,
                                boxstyle=f"round,pad=0,rounding_size={0.04*s:.4f}",
                                facecolor="white", edgecolor="none"))
    # crossbones (tiny)
    for ang in (35, -35):
        tr = Affine2D().rotate_deg(ang).translate(cx, cy-0.42*s) + ax.transData
        ax.add_patch(FancyBboxPatch((-0.62*s,-0.055*s), 1.24*s, 0.11*s,
                                    boxstyle=f"round,pad=0,rounding_size={0.05*s:.4f}",
                                    facecolor="white", edgecolor="none", transform=tr))
        for end in (-0.6*s, 0.6*s):
            ax.add_patch(Circle((end,0), 0.085*s, facecolor="white",
                                edgecolor="none", transform=tr))
    # eye sockets (black)
    for sx in (-0.17*s, 0.17*s):
        ax.add_patch(Ellipse((cx+sx, cy+0.185*s), 0.22*s, 0.25*s,
                             facecolor="black", edgecolor="none"))
    ax.add_patch(Polygon([[cx,cy+0.035*s],[cx-0.07*s,cy-0.07*s],[cx+0.07*s,cy-0.07*s]],
                          closed=True, facecolor="black", edgecolor="none"))
    for x in (-0.13*s, 0.0, 0.13*s):
        ax.add_patch(FancyBboxPatch((cx+x-0.028*s,cy-0.205*s), 0.056*s, 0.115*s,
                                    facecolor="black", edgecolor="none"))


def draw():
    """Spider webs with skull-and-crossbones at the centre instead of a spider, 7×7."""
    fig, ax = setup_ax()
    cols, rows = 7, 7
    dx, dy = PERIOD/cols, PERIOD/rows
    r = min(dx, dy) * 0.58
    for row in range(rows):
        for col in range(cols):
            cx = (col+0.5)*dx + (dx*0.5 if row%2 else 0)
            cy = (row+0.5)*dy
            for ox, oy in WRAPS:
                web_skull(ax, cx+ox, cy+oy, r)
    save(fig, "abstract halloween variation cobweb skull centre face instead spider pattern black white texture")


if __name__ == "__main__":
    draw()
