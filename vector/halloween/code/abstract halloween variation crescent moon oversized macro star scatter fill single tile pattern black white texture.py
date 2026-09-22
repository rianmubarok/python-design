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


def draw_crescent(ax, cx, cy, r_outer, tilt, color="white"):
    n = 200
    offset_dist = r_outer * 0.42
    theta_out = np.linspace(-np.pi * 0.60, np.pi * 0.60, n)
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
                         closed=True, facecolor=color, edgecolor="none"))


def draw_star(ax, cx, cy, r_outer, r_inner, n_pts, angle_offset=0.0, color="white"):
    """N-pointed star polygon."""
    angles = np.linspace(0, 2 * np.pi, n_pts * 2, endpoint=False) + angle_offset
    radii = np.tile([r_outer, r_inner], n_pts)
    xs = cx + radii * np.cos(angles)
    ys = cy + radii * np.sin(angles)
    ax.add_patch(Polygon(np.column_stack([xs, ys]), closed=True,
                         facecolor=color, edgecolor="none"))


def draw():
    """2×2 macro crescent tiles. Each tile: one giant crescent + scattered stars.
    Stars are defined in absolute canvas space [0, PERIOD) so they tile seamlessly
    via WRAPS — no star is cut off at an edge without a matching copy."""
    fig, ax = setup_ax()

    cols, rows = 2, 2
    dx, dy = PERIOD / cols, PERIOD / rows
    r_crescent = min(dx, dy) * 0.40

    # Single tilt for all tiles — same angle everywhere = seamless repeat
    tilt = np.radians(20)

    # --- Stars: absolute positions in [0, PERIOD) ---
    rng = np.random.default_rng(42)
    n_stars = 28  # more stars since they cover 2×2 tiles
    star_ax = rng.uniform(0.0, PERIOD, n_stars)   # absolute x
    star_ay = rng.uniform(0.0, PERIOD, n_stars)   # absolute y
    star_sizes = rng.uniform(0.012, 0.032, n_stars) * PERIOD
    star_pts = rng.choice([4, 5, 6], n_stars)

    # Draw crescents (per tile hub, wrapped)
    for row in range(-1, rows + 1):
        for col in range(-1, cols + 1):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -25 <= px <= PERIOD + 25 and -25 <= py <= PERIOD + 25:
                    draw_crescent(ax, px, py, r_crescent, tilt)

    # Draw stars (absolute positions, each wrapped to cover all edges)
    for i in range(n_stars):
        sr = star_sizes[i]
        for ox, oy in WRAPS:
            sx = star_ax[i] + ox
            sy = star_ay[i] + oy
            if -sr <= sx <= PERIOD + sr and -sr <= sy <= PERIOD + sr:
                draw_star(ax, sx, sy, sr, sr * 0.42, int(star_pts[i]),
                          angle_offset=np.radians(i * 17))

    save(fig, "abstract halloween variation crescent moon oversized macro star scatter fill single tile pattern black white texture")


if __name__ == "__main__":
    draw()
