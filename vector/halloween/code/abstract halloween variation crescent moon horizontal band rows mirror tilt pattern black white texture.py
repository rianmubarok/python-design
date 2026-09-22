import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI  = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR  = SCRIPT_DIR.parent / "output"
JPG_DIR     = OUTPUT_DIR / "jpg"
SVG_DIR     = OUTPUT_DIR / "svg"
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


def draw_crescent(ax, cx, cy, r_outer, tilt):
    n_pts = 160
    offset_dist = r_outer * 0.42
    theta_outer = np.linspace(-np.pi * 0.58, np.pi * 0.58, n_pts)
    outer_x = cx + r_outer * np.cos(theta_outer)
    outer_y = cy + r_outer * np.sin(theta_outer)
    punch_cx, punch_cy = cx + offset_dist, cy
    p1 = (outer_x[-1] - punch_cx, outer_y[-1] - punch_cy)
    p2 = (outer_x[0]  - punch_cx, outer_y[0]  - punch_cy)
    angle1, angle2 = np.arctan2(p1[1], p1[0]), np.arctan2(p2[1], p2[0])
    theta_inner = np.linspace(angle1, angle2, n_pts)
    r_in = np.hypot(p1[0], p1[1])
    inner_x = punch_cx + r_in * np.cos(theta_inner)
    inner_y = punch_cy + r_in * np.sin(theta_inner)
    pts_x = np.concatenate([outer_x, inner_x]) - cx
    pts_y = np.concatenate([outer_y, inner_y]) - cy
    rot_x = pts_x * np.cos(tilt) - pts_y * np.sin(tilt) + cx
    rot_y = pts_x * np.sin(tilt) + pts_y * np.cos(tilt) + cy
    ax.add_patch(Polygon(np.column_stack([rot_x, rot_y]),
                         closed=True, facecolor="white", edgecolor="none"))


def draw():
    """Horizontal band layout: 5 cols × 6 rows of crescents.
    Each row has a fixed tilt; adjacent rows mirror each other (positive/negative).
    Tightly packed, no stagger — pure stripe/band rhythm.
    """
    fig, ax = setup_ax()
    cols, rows = 5, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    r = min(dx, dy) * 0.40

    # Row tilt sequence: alternate between upward-left and upward-right lean
    row_tilts = [np.radians(t) for t in [30, -30, 50, -50, 15, -15]]

    for row in range(rows):
        tilt = row_tilts[row % len(row_tilts)]
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                draw_crescent(ax, cx + ox, cy + oy, r, tilt)

    save(fig,
         "abstract halloween variation crescent moon horizontal band rows "
         "mirror tilt pattern black white texture")


if __name__ == "__main__":
    draw()
