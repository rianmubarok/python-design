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
    """Standard crescent silhouette."""
    n = 160
    offset_dist = r_outer * 0.42
    theta_out = np.linspace(-np.pi * 0.60, np.pi * 0.60, n)
    ox = cx + r_outer * np.cos(theta_out)
    oy = cy + r_outer * np.sin(theta_out)
    punch_cx = cx + offset_dist
    p1 = (ox[-1]-punch_cx, oy[-1]-cy)
    p2 = (ox[0] -punch_cx, oy[0] -cy)
    a1 = np.arctan2(p1[1], p1[0])
    a2 = np.arctan2(p2[1], p2[0])
    ri = np.hypot(p1[0], p1[1])
    t_i = np.linspace(a1, a2, n)
    ix = punch_cx + ri*np.cos(t_i)
    iy = cy + ri*np.sin(t_i)
    px = np.concatenate([ox, ix]) - cx
    py = np.concatenate([oy, iy]) - cy
    rx = px*np.cos(tilt) - py*np.sin(tilt) + cx
    ry = px*np.sin(tilt) + py*np.cos(tilt) + cy
    ax.add_patch(Polygon(np.column_stack([rx, ry]),
                         closed=True, facecolor="white", edgecolor="none"))


def draw():
    """3×3 tile of crescent-ripple expansions.
    Each hub has 6 concentric rings of crescents at increasing radii — like ripples.
    Each ring's crescents are rotated to face outward radially.
    Innermost ring = 4 crescents, outer rings add 2 more each.
    White on black — creates an elegant expanding-wave feel."""
    fig, ax = setup_ax()

    cols, rows = 3, 3
    dx, dy = PERIOD / cols, PERIOD / rows
    r_crescent = min(dx, dy) * 0.066

    rings = [
        dict(n=4,  orbit=0.00, add_a=0.0),   # centre single
        dict(n=5,  orbit=0.14, add_a=0.0),
        dict(n=7,  orbit=0.24, add_a=0.0),
        dict(n=9,  orbit=0.34, add_a=0.0),
        dict(n=11, orbit=0.44, add_a=0.0),
    ]

    for row in range(-1, rows + 1):
        for col in range(-1, cols + 1):
            hub_x = (col + 0.5) * dx
            hub_y = (row + 0.5) * dy
            rot0 = np.radians(22) if (row+col) % 2 else 0.0

            for ox, oy in WRAPS:
                px, py = hub_x + ox, hub_y + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    for ring in rings:
                        n = ring['n']
                        orb = ring['orbit'] * min(dx, dy)
                        for k in range(n):
                            a = rot0 + k * 2*np.pi / n
                            cx2 = px + orb * np.cos(a)
                            cy2 = py + orb * np.sin(a)
                            # tilt crescent to face outward
                            tilt = a + np.pi/2
                            draw_crescent(ax, cx2, cy2, r_crescent, tilt)

    save(fig, "abstract halloween variation crescent moon concentric wave ripple rings expanding pattern black white texture")


if __name__ == "__main__":
    draw()
