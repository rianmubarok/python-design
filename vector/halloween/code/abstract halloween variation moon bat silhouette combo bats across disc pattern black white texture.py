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


def bat_poly(cx, cy, s, angle=0.0):
    pts = np.array([
        [0.00,  0.08], [0.12,  0.18], [0.10,  0.05], [0.42,  0.22], [0.78,  0.38],
        [0.62,  0.08], [0.95,  0.12], [0.55, -0.08], [0.72, -0.28], [0.28, -0.10],
        [0.18, -0.22], [0.08, -0.08], [0.00, -0.18],
        [-0.08,-0.08], [-0.18,-0.22], [-0.28,-0.10], [-0.72,-0.28],
        [-0.55,-0.08], [-0.95, 0.12], [-0.62, 0.08], [-0.78, 0.38],
        [-0.42, 0.22], [-0.10, 0.05], [-0.12, 0.18],
    ]) * s
    c, s_ = np.cos(angle), np.sin(angle)
    R = np.array([[c, -s_],[s_, c]])
    return (R @ pts.T).T + [cx, cy]


def moon_tile(ax, cx, cy, moon_r, rng):
    """Full moon disc (white) with 3–6 black bat silhouettes flying across it."""
    ax.add_patch(Circle((cx, cy), moon_r, facecolor="white", edgecolor="none", zorder=2))
    # subtle craters
    for _ in range(rng.integers(3, 6)):
        cr = moon_r * rng.uniform(0.04, 0.10)
        ca = rng.uniform(0, 2 * np.pi)
        cd = moon_r * rng.uniform(0.1, 0.72)
        ax.add_patch(Circle((cx + cd * np.cos(ca), cy + cd * np.sin(ca)),
                            cr, facecolor="none",
                            edgecolor="black", linewidth=0.35, alpha=0.35, zorder=3))
    # bats
    n_bats = rng.integers(3, 7)
    for _ in range(n_bats):
        # random position within moon disc
        dist = rng.uniform(0, moon_r * 0.76)
        ang = rng.uniform(0, 2 * np.pi)
        bx = cx + dist * np.cos(ang)
        by = cy + dist * np.sin(ang)
        bs = moon_r * rng.uniform(0.10, 0.22)
        b_angle = rng.uniform(-0.3, 0.3)
        ax.add_patch(Polygon(bat_poly(bx, by, bs, b_angle), closed=True,
                             facecolor="black", edgecolor="none", zorder=4))


def draw():
    """4×4 full moon tiles, each with bats flying across the disc. Black background."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(31)
    cols, rows = 4, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    moon_r = min(dx, dy) * 0.44
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                moon_tile(ax, cx + ox, cy + oy, moon_r, rng)
    save(fig, "abstract halloween variation moon bat silhouette combo bats across disc pattern black white texture")


if __name__ == "__main__":
    draw()
