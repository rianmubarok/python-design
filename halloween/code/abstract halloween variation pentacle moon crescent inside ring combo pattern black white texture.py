import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
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
EPS_DIR = OUTPUT_DIR / \"eps\"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


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
    eps_path = EPS_DIR / f\"{name} {DATE}.eps\"
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format=\"eps\", pad_inches=0, facecolor=\"white\", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path} | {eps_path}")


def pentacle_moon(ax, cx, cy, r):
    """Pentagram star + surrounding circle, with a crescent moon inside."""
    # outer circle
    ax.add_patch(Circle((cx, cy), r, facecolor="none",
                        edgecolor="white", linewidth=0.8))
    # pentagram
    pts = []
    for i in range(5):
        a = -np.pi/2 + i*2*np.pi/5
        pts.append([cx+r*0.92*np.cos(a), cy+r*0.92*np.sin(a)])
    order = [0, 2, 4, 1, 3]
    star = np.array([pts[j] for j in order])
    ax.add_patch(Polygon(star, closed=True, facecolor="none",
                         edgecolor="white", linewidth=0.7))

    # inner circle (smaller ring inside star)
    inner_r = r * 0.38
    ax.add_patch(Circle((cx, cy), inner_r, facecolor="none",
                        edgecolor="white", linewidth=0.5))

    # crescent inside the inner circle
    cr = inner_r * 0.82
    ax.add_patch(Circle((cx, cy), cr, facecolor="white", edgecolor="none", zorder=2))
    ax.add_patch(Circle((cx + cr*0.52, cy + cr*0.18), cr*0.74,
                        facecolor="black", edgecolor="none", zorder=3))


def draw():
    """5×5 pentacle-moon combo tiles — star with crescent inside each ring."""
    fig, ax = setup_ax()
    cols, rows = 5, 5
    dx, dy = PERIOD/cols, PERIOD/rows
    r = min(dx, dy) * 0.46
    for row in range(rows):
        for col in range(cols):
            cx = (col+0.5)*dx
            cy = (row+0.5)*dy
            for ox, oy in WRAPS:
                pentacle_moon(ax, cx+ox, cy+oy, r)
    save(fig, "abstract halloween variation pentacle moon crescent inside ring combo pattern black white texture")


if __name__ == "__main__":
    draw()
