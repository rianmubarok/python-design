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


def draw_crescent(ax, cx, cy, r, tilt, fill="white"):
    n = 160
    offset = r * 0.40
    t_out = np.linspace(-np.pi * 0.62, np.pi * 0.62, n)
    ox_pts = r * np.cos(t_out)
    oy_pts = r * np.sin(t_out)
    punch_x = offset
    p1 = (ox_pts[-1] - punch_x, oy_pts[-1])
    p2 = (ox_pts[0]  - punch_x, oy_pts[0])
    a1 = np.arctan2(p1[1], p1[0])
    a2 = np.arctan2(p2[1], p2[0])
    r_in = np.hypot(p1[0], p1[1])
    t_in = np.linspace(a1, a2, n)
    ix_pts = punch_x + r_in * np.cos(t_in)
    iy_pts = r_in * np.sin(t_in)
    # rotate by tilt then translate
    all_x = np.concatenate([ox_pts, ix_pts])
    all_y = np.concatenate([oy_pts, iy_pts])
    rx = all_x * np.cos(tilt) - all_y * np.sin(tilt) + cx
    ry = all_x * np.sin(tilt) + all_y * np.cos(tilt) + cy
    ax.add_patch(Polygon(np.column_stack([rx, ry]), closed=True,
                         facecolor=fill, edgecolor="none", zorder=2))


def draw_cluster(ax, cx, cy, n_moons, base_r, spoke_dist, rng):
    """Radial burst: n_moons crescents arranged around a centre,
    each pointing outward from the hub. Sizes decrease with orbit index."""
    angles = np.linspace(0, 2 * np.pi, n_moons, endpoint=False)
    angles += rng.uniform(0, 2 * np.pi)  # random start rotation per cluster
    for k, ang in enumerate(angles):
        r_scale = 1.0 - k * 0.04          # very slight size decrease
        r = base_r * r_scale
        dist = spoke_dist + k * base_r * 0.15
        mcx = cx + dist * np.cos(ang)
        mcy = cy + dist * np.sin(ang)
        # tilt: crescent points outward from cluster centre
        tilt = ang + np.pi * 0.5
        draw_crescent(ax, mcx, mcy, r, tilt, fill="white")


def draw():
    """Scattered clusters of 5–7 radially-burst crescents on a staggered grid.
    Each cluster looks like a bloom or starburst of moons. Seamless."""
    fig, ax = setup_ax()

    cols, rows = 4, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    base_r = min(dx, dy) * 0.130
    spoke = min(dx, dy) * 0.190
    rng = np.random.default_rng(7)

    n_moons_seq = [5, 6, 7, 5, 6, 7, 5, 6, 7, 6, 5, 7, 6, 5, 7, 6]
    idx = 0
    for row in range(rows):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(cols):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            n_m = n_moons_seq[idx % len(n_moons_seq)]
            idx += 1
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    draw_cluster(ax, px, py, n_m, base_r, spoke, rng)

    save(fig, "abstract halloween variation crescent moon cluster radial burst scattered field pattern black white texture")


if __name__ == "__main__":
    draw()
