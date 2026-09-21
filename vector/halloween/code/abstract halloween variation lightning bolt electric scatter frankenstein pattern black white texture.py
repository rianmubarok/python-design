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


def lightning_bolt(ax, cx, cy, height, width, angle_deg=0, fill="white"):
    """Classic Z-shaped lightning bolt — solid filled polygon."""
    h = height
    w = width
    pts = np.array([
        [-w * 0.10,  h * 0.50],
        [ w * 0.50,  h * 0.50],
        [ w * 0.05,  h * 0.04],
        [ w * 0.45,  h * 0.04],
        [ w * 0.10, -h * 0.50],
        [-w * 0.50, -h * 0.50],
        [-w * 0.05, -h * 0.04],
        [-w * 0.45, -h * 0.04],
    ])
    a = np.radians(angle_deg)
    c, s_ = np.cos(a), np.sin(a)
    R = np.array([[c, -s_], [s_, c]])
    pts = (R @ pts.T).T + [cx, cy]
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor="none"))


def branching_bolt(ax, cx, cy, height, width, angle_deg=0, depth=2, rng=None):
    """Recursive branching bolt."""
    if rng is None:
        rng = np.random.default_rng()
    lightning_bolt(ax, cx, cy, height, width, angle_deg, fill="white")
    if depth > 0:
        for _ in range(rng.integers(1, 3)):
            branch_angle = angle_deg + rng.uniform(-45, 45)
            branch_h = height * rng.uniform(0.40, 0.62)
            branch_w = width  * rng.uniform(0.35, 0.55)
            t  = rng.uniform(0.2, 0.7)
            bx = cx + t * height * 0.3 * np.cos(np.radians(angle_deg))
            by = cy - t * height * 0.5 * np.sin(np.radians(angle_deg + 90))
            branching_bolt(ax, bx, by, branch_h, branch_w,
                           branch_angle, depth - 1, rng)


def draw():
    """Dense scatter of lightning bolts — varying sizes, angles, with branching.
    Jittered 9×9 grid on black background."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)
    cols, rows = 9, 9
    dx, dy = PERIOD / cols, PERIOD / rows

    for row in range(rows):
        for col in range(cols):
            jx = rng.uniform(0.08, 0.92) * dx
            jy = rng.uniform(0.08, 0.92) * dy
            cx = col * dx + jx
            cy = row * dy + jy
            h  = rng.uniform(3.5, 8.0)
            w  = h * rng.uniform(0.40, 0.65)
            ang = rng.uniform(-30, 30)
            use_branch = rng.random() < 0.30
            for ox, oy in WRAPS:
                if use_branch:
                    branching_bolt(ax, cx+ox, cy+oy, h, w, ang, depth=1, rng=rng)
                else:
                    lightning_bolt(ax, cx+ox, cy+oy, h, w, ang)

    save(fig, "abstract halloween variation lightning bolt electric scatter frankenstein pattern black white texture")


if __name__ == "__main__":
    draw()
