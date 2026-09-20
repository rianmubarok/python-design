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
    print(f"Saved: {jpg_path}")


def skull(ax, cx, cy, s, fill="white", inv="black"):
    for ang in (35, -35):
        tr = Affine2D().rotate_deg(ang).translate(cx, cy - 0.42*s) + ax.transData
        ax.add_patch(FancyBboxPatch(
            (-0.62*s, -0.055*s), 1.24*s, 0.11*s,
            boxstyle=f"round,pad=0,rounding_size={0.05*s:.4f}",
            facecolor=fill, edgecolor="none", transform=tr))
        for end in (-0.6*s, 0.6*s):
            ax.add_patch(Circle((end, 0), 0.085*s, facecolor=fill,
                                edgecolor="none", transform=tr))
    ax.add_patch(Ellipse((cx, cy+0.16*s), 0.82*s, 0.74*s, facecolor=fill, edgecolor="none"))
    ax.add_patch(FancyBboxPatch(
        (cx-0.26*s, cy-0.24*s), 0.52*s, 0.26*s,
        boxstyle=f"round,pad=0,rounding_size={0.04*s:.4f}",
        facecolor=fill, edgecolor="none"))
    for sx in (-0.17*s, 0.17*s):
        ax.add_patch(Ellipse((cx+sx, cy+0.185*s), 0.22*s, 0.25*s,
                             facecolor=inv, edgecolor="none"))
    ax.add_patch(Polygon(
        [[cx,cy+0.035*s],[cx-0.07*s,cy-0.07*s],[cx+0.07*s,cy-0.07*s]],
        closed=True, facecolor=inv, edgecolor="none"))
    for x in (-0.13*s, 0.0, 0.13*s):
        ax.add_patch(FancyBboxPatch(
            (cx+x-0.028*s, cy-0.205*s), 0.056*s, 0.115*s,
            facecolor=inv, edgecolor="none"))


def blood_drip(ax, cx, top_y, drop_r, tail_len, fill="white"):
    """Drip hanging downward from top_y."""
    by = top_y - tail_len
    ax.add_patch(Circle((cx, by), drop_r, facecolor=fill, edgecolor="none"))
    tail_pts = [
        (cx - drop_r*0.35, by + drop_r*0.75),
        (cx - 0.4, top_y + drop_r*0.2),
        (cx, top_y),
        (cx + 0.4, top_y + drop_r*0.2),
        (cx + drop_r*0.35, by + drop_r*0.75),
    ]
    ax.add_patch(Polygon(tail_pts, closed=True, facecolor=fill, edgecolor="none"))


def draw():
    """White skulls on black, each with 3–4 blood drips hanging from the jaw."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(44)
    cols, rows = 5, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.54
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy + s * 0.12   # shift up slightly to leave drip space
            jaw_y = cy - 0.48 * s               # bottom of jaw
            for ox, oy in WRAPS:
                skull(ax, cx+ox, cy+oy, s)
                # 3–4 drips from jaw baseline
                n_drips = rng.integers(3, 5)
                drip_xs = np.linspace(cx - 0.22*s, cx + 0.22*s, n_drips)
                for dx2 in drip_xs:
                    dr = rng.uniform(0.8, 1.4)
                    tl = rng.uniform(2.0, 5.5)
                    blood_drip(ax, dx2+ox, jaw_y+oy, dr, tl)
    save(fig, "abstract halloween variation skull drip blood drops hanging combo pattern black white texture")


if __name__ == "__main__":
    draw()
