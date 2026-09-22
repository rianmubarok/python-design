import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse
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
    """Simple crescent moon polygon."""
    n = 180
    offset = r * 0.42
    theta_out = np.linspace(-np.pi * 0.62, np.pi * 0.62, n)
    ox_pts = cx + r * np.cos(theta_out)
    oy_pts = cy + r * np.sin(theta_out)

    punch_cx = cx + offset
    punch_cy = cy
    p1 = (ox_pts[-1] - punch_cx, oy_pts[-1] - punch_cy)
    p2 = (ox_pts[0]  - punch_cx, oy_pts[0]  - punch_cy)
    a1 = np.arctan2(p1[1], p1[0])
    a2 = np.arctan2(p2[1], p2[0])
    r_inner = np.hypot(p1[0], p1[1])
    theta_in = np.linspace(a1, a2, n)
    ix_pts = punch_cx + r_inner * np.cos(theta_in)
    iy_pts = punch_cy + r_inner * np.sin(theta_in)

    pts_x = np.concatenate([ox_pts, ix_pts]) - cx
    pts_y = np.concatenate([oy_pts, iy_pts]) - cy
    rx = pts_x * np.cos(tilt) - pts_y * np.sin(tilt) + cx
    ry = pts_x * np.sin(tilt) + pts_y * np.cos(tilt) + cy
    ax.add_patch(Polygon(np.column_stack([rx, ry]), closed=True,
                         facecolor=fill, edgecolor="none", zorder=2))


def draw_bat(ax, cx, cy, s, fill="white"):
    """Simple geometric bat silhouette."""
    body_pts = [
        (0, 0.18 * s), (0.07 * s, 0.06 * s), (0, -0.10 * s),
        (-0.07 * s, 0.06 * s)
    ]
    # left wing
    lwing = [
        (0, 0.10 * s), (-0.18 * s, 0.22 * s), (-0.38 * s, 0.08 * s),
        (-0.42 * s, -0.10 * s), (-0.26 * s, -0.16 * s),
        (-0.14 * s, -0.04 * s), (0, 0.0)
    ]
    # right wing (mirror)
    rwing = [(-x, y) for x, y in lwing]

    for poly in [body_pts, lwing, rwing]:
        shifted = [(cx + px, cy + py) for px, py in poly]
        ax.add_patch(Polygon(shifted, closed=True,
                             facecolor=fill, edgecolor="none", zorder=3))


def draw():
    """Scattered paired duo: each tile unit = one crescent moon + one orbiting bat.
    Crescent moons on a staggered 4×5 grid; bat placed at orbital position
    around the moon varying by tile position. White on black background."""
    fig, ax = setup_ax()

    cols, rows = 4, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    moon_r = min(dx, dy) * 0.26
    bat_s  = moon_r * 0.55

    # Orbital angles cycling through tiles for visual variety
    orbit_angles = np.radians([45, 135, 225, 315, 30, 150, 210, 330,
                                60, 120, 240, 300, 80, 160, 200, 280,
                                20, 100, 260, 340])
    moon_tilts = np.radians([20, 340, 55, 305, 15, 345, 70, 290,
                              40, 320, 50, 310, 25, 335, 65, 295,
                              10, 350, 45, 315])
    idx = 0
    for row in range(rows):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(cols):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            tilt = moon_tilts[idx % len(moon_tilts)]
            orb_a = orbit_angles[idx % len(orbit_angles)]
            idx += 1

            # Orbital distance = just outside the moon
            orb_dist = moon_r * 1.55
            bat_cx = cx + orb_dist * np.cos(orb_a)
            bat_cy = cy + orb_dist * np.sin(orb_a)

            for ox, oy in WRAPS:
                mx, my = cx + ox, cy + oy
                bx, by = bat_cx + ox, bat_cy + oy
                if -15 <= mx <= PERIOD + 15 and -15 <= my <= PERIOD + 15:
                    draw_crescent(ax, mx, my, moon_r, tilt, fill="white")
                if -15 <= bx <= PERIOD + 15 and -15 <= by <= PERIOD + 15:
                    draw_bat(ax, bx, by, bat_s, fill="white")

    save(fig, "abstract halloween variation bat orbit crescent moon paired duo scattered pattern black white texture")


if __name__ == "__main__":
    draw()
