import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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


def draw_crescent(ax, cx, cy, r_outer, tilt):
    """Slim crescent: inner circle offset is 65% of outer radius → narrow sliver."""
    n = 180
    offset_dist = r_outer * 0.65

    theta_out = np.linspace(-np.pi * 0.55, np.pi * 0.55, n)
    ox = cx + r_outer * np.cos(theta_out)
    oy = cy + r_outer * np.sin(theta_out)

    punch_cx = cx + offset_dist
    punch_cy = cy

    p1 = (ox[-1] - punch_cx, oy[-1] - punch_cy)
    p2 = (ox[0]  - punch_cx, oy[0]  - punch_cy)
    a1 = np.arctan2(p1[1], p1[0])
    a2 = np.arctan2(p2[1], p2[0])
    r_in = np.hypot(p1[0], p1[1])

    theta_in = np.linspace(a1, a2, n)
    ix = punch_cx + r_in * np.cos(theta_in)
    iy = punch_cy + r_in * np.sin(theta_in)

    pts_x = np.concatenate([ox, ix]) - cx
    pts_y = np.concatenate([oy, iy]) - cy

    rot_x = pts_x * np.cos(tilt) - pts_y * np.sin(tilt) + cx
    rot_y = pts_x * np.sin(tilt) + pts_y * np.cos(tilt) + cy

    ax.add_patch(Polygon(np.column_stack([rot_x, rot_y]),
                         closed=True, facecolor="white", edgecolor="none"))


def draw():
    """Tight horizontal rows of slim crescent slivers, alternating angle +35°/−35°.
    Many crescents per row — dense band stripe effect."""
    fig, ax = setup_ax()

    rows = 8
    crescents_per_row = 7
    dy = PERIOD / rows
    dx = PERIOD / crescents_per_row
    r = min(dx, dy) * 0.46

    tilt_a = np.radians(35)
    tilt_b = np.radians(-35)

    for row in range(-1, rows + 1):
        tilt = tilt_a if row % 2 == 0 else tilt_b
        shift = (dx * 0.5) if row % 2 else 0.0
        cy = (row + 0.5) * dy
        for col in range(-1, crescents_per_row + 2):
            cx = (col + 0.5) * dx + shift
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -10 <= px <= PERIOD + 10 and -10 <= py <= PERIOD + 10:
                    draw_crescent(ax, px, py, r, tilt)

    save(fig, "abstract halloween variation crescent moon slim sliver angled horizontal band rows pattern black white texture")


if __name__ == "__main__":
    draw()
