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


def pentagram_pts(cx, cy, r):
    pts = []
    for i in range(5):
        a = -np.pi/2 + i*2*np.pi/5
        pts.append([cx+r*np.cos(a), cy+r*np.sin(a)])
    # connect star order: 0-2-4-1-3-0
    order = [0, 2, 4, 1, 3]
    return np.array([pts[i] for i in order])


def nested_pentacles(ax, cx, cy, max_r, n_levels=4):
    """Concentric pentagram stars, alternating filled/outline, decreasing scale."""
    for i in range(n_levels):
        r = max_r * (0.9 ** i)
        rot = i * np.radians(18)   # rotate each level slightly
        pts = []
        for k in range(5):
            a = -np.pi/2 + rot + k*2*np.pi/5
            pts.append([cx+r*np.cos(a), cy+r*np.sin(a)])
        order = [0, 2, 4, 1, 3]
        star = np.array([pts[j] for j in order])
        fill = "white" if i % 2 == 0 else "none"
        ec = "none" if i % 2 == 0 else "white"
        ax.add_patch(Polygon(star, closed=True, facecolor=fill,
                             edgecolor=ec, linewidth=0.7))
        # surrounding circle
        ax.add_patch(Circle((cx, cy), r, facecolor="none",
                            edgecolor="white", linewidth=0.4, alpha=0.5))


def draw():
    """4×4 tiles of nested concentric pentacles, 4 levels deep per tile."""
    fig, ax = setup_ax()
    cols, rows = 4, 4
    dx, dy = PERIOD/cols, PERIOD/rows
    r = min(dx, dy) * 0.46
    for row in range(rows):
        for col in range(cols):
            cx = (col+0.5)*dx
            cy = (row+0.5)*dy
            for ox, oy in WRAPS:
                nested_pentacles(ax, cx+ox, cy+oy, r, n_levels=4)
    save(fig, "abstract halloween variation pentacle nested concentric decreasing scale pattern black white texture")


if __name__ == "__main__":
    draw()
