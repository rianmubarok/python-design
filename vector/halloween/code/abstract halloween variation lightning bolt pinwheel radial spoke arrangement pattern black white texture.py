import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Polygon, Circle
from matplotlib.path import Path as MPath
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


def lightning_bolt_pts(length, width):
    """Return local (centred at 0,0) points of a zigzag lightning bolt pointing up."""
    w = width
    h = length
    # Classic 2-kink zigzag bolt
    pts = np.array([
        [w * 0.05,  h * 0.50],    # top-right
        [-w * 0.05, h * 0.50],    # top-left
        [-w * 0.30, h * 0.08],    # mid-left upper
        [w * 0.05,  h * 0.08],    # mid-right upper (kink)
        [-w * 0.05, -h * 0.08],   # mid-left lower
        [w * 0.30,  -h * 0.08],   # mid-right lower (kink)
        [w * 0.05,  -h * 0.50],   # bottom-right
        [-w * 0.05, -h * 0.50],   # bottom-left
        [w * 0.10,  -h * 0.06],
        [-w * 0.10, -h * 0.06],
        [w * 0.10,  h * 0.06],
        [-w * 0.20, h * 0.06],
    ])
    # Simpler clean bolt shape
    pts = np.array([
        [ w * 0.10,  h * 0.50],
        [-w * 0.25,  h * 0.05],
        [ w * 0.12,  h * 0.05],
        [-w * 0.10, -h * 0.50],
        [ w * 0.25, -h * 0.05],
        [-w * 0.12, -h * 0.05],
    ])
    return pts


def draw_bolt(ax, cx, cy, length, width, angle=0.0, fill="white"):
    pts = lightning_bolt_pts(length, width)
    rot = np.array([[np.cos(angle), -np.sin(angle)],
                    [np.sin(angle),  np.cos(angle)]])
    rpts = (rot @ pts.T).T
    rpts[:, 0] += cx
    rpts[:, 1] += cy
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(rpts) - 2) + [MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(rpts, codes), facecolor=fill, edgecolor="none", zorder=2))


def pinwheel_bolts(ax, cx, cy, orbit_r, bolt_l, bolt_w, n=6, angle_offset=0.0, fill="white"):
    """Place n bolts radially, each pointing outward from hub."""
    for k in range(n):
        a = angle_offset + k * 2 * np.pi / n
        bx = cx + orbit_r * np.cos(a)
        by = cy + orbit_r * np.sin(a)
        draw_bolt(ax, bx, by, bolt_l, bolt_w, angle=a, fill=fill)


def draw():
    """3×3 tiles of lightning bolt pinwheels.
    Each hub has 6 bolts radiating outward + hub dot.
    Alternate tiles offset by half step for dynamic feel."""
    fig, ax = setup_ax()

    cols, rows = 3, 3
    dx, dy = PERIOD / cols, PERIOD / rows
    orbit_r = min(dx, dy) * 0.28
    bolt_l  = min(dx, dy) * 0.26
    bolt_w  = bolt_l * 0.32

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            ao = np.radians(30) if (row + col) % 2 else 0.0
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    pinwheel_bolts(ax, px, py, orbit_r, bolt_l, bolt_w,
                                   n=6, angle_offset=ao, fill="white")
                    ax.add_patch(Circle((px, py), bolt_w * 0.6,
                                       facecolor="white", edgecolor="none", zorder=3))

    save(fig, "abstract halloween variation lightning bolt pinwheel radial spoke arrangement pattern black white texture")


if __name__ == "__main__":
    draw()
