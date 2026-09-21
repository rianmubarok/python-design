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


def skull_mini(ax, cx, cy, s):
    ax.add_patch(Ellipse((cx,cy+0.16*s),0.82*s,0.74*s,facecolor="black",edgecolor="none"))
    ax.add_patch(FancyBboxPatch((cx-0.26*s,cy-0.24*s),0.52*s,0.26*s,
                                boxstyle=f"round,pad=0,rounding_size={0.04*s:.4f}",
                                facecolor="black",edgecolor="none"))
    for sx in (-0.17*s,0.17*s):
        ax.add_patch(Ellipse((cx+sx,cy+0.185*s),0.22*s,0.25*s,facecolor="white",edgecolor="none"))
    ax.add_patch(Polygon([[cx,cy+0.035*s],[cx-0.07*s,cy-0.07*s],[cx+0.07*s,cy-0.07*s]],
                          closed=True,facecolor="white",edgecolor="none"))
    for x in (-0.13*s,0.0,0.13*s):
        ax.add_patch(FancyBboxPatch((cx+x-0.028*s,cy-0.205*s),0.056*s,0.115*s,
                                    facecolor="white",edgecolor="none"))


def draw():
    """Argyle diamond grid with small skulls at intersection points."""
    fig, ax = setup_ax()
    step = PERIOD / 7.0
    skull_s = step * 0.28

    # draw argyle diamonds (alternating black/white fill)
    rows_d, cols_d = 9, 9
    for row in range(rows_d):
        for col in range(cols_d):
            cx = (col + (0.5 if row%2 else 0)) * step
            cy = row * step * 0.5
            fill = "black" if (row+col)%2==0 else "white"
            edge = "none" if fill=="black" else "black"
            # rotated square = argyle diamond
            diamond = np.array([
                [cx,         cy+step*0.5],
                [cx+step*0.5,cy],
                [cx,         cy-step*0.5],
                [cx-step*0.5,cy],
            ])
            for ox, oy in WRAPS:
                ax.add_patch(Polygon(diamond+[ox,oy], closed=True,
                                     facecolor=fill, edgecolor=edge, linewidth=0.5))

    # diagonal crossing lines
    for i in range(-2, 12):
        t = np.linspace(-5, PERIOD+5, 2)
        ax.plot(t, t - i*step + PERIOD/2, color="black", linewidth=0.4, alpha=0.35)
        ax.plot(t, -t + i*step + PERIOD/2, color="black", linewidth=0.4, alpha=0.35)

    # skulls at grid intersections
    for row in range(rows_d):
        for col in range(cols_d):
            cx = (col + (0.5 if row%2 else 0)) * step
            cy = row * step * 0.5
            for ox, oy in WRAPS:
                skull_mini(ax, cx+ox, cy+oy, skull_s)
    save(fig, "abstract halloween variation skull argyle diamond intersection grid pattern black white texture")


if __name__ == "__main__":
    draw()
