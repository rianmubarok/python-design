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


def bat_poly_pts(cx, cy, s):
    pts = np.array([
        [0.00,  0.08],[0.12,  0.18],[0.10,  0.05],[0.42,  0.22],[0.78,  0.38],
        [0.62,  0.08],[0.95,  0.12],[0.55, -0.08],[0.72, -0.28],[0.28, -0.10],
        [0.18, -0.22],[0.08, -0.08],[0.00, -0.18],
        [-0.08,-0.08],[-0.18,-0.22],[-0.28,-0.10],[-0.72,-0.28],
        [-0.55,-0.08],[-0.95, 0.12],[-0.62, 0.08],[-0.78, 0.38],
        [-0.42, 0.22],[-0.10, 0.05],[-0.12, 0.18],
    ]) * s + [cx, cy]
    return pts


def moon_bat_cutout(ax, cx, cy, moon_r, n_bats=3):
    """White moon disc with black bat silhouettes cut out as negative space.
    Achieved by drawing moon (white), then black bats on top."""
    # White moon
    ax.add_patch(Circle((cx, cy), moon_r, facecolor="white", edgecolor="none", zorder=2))
    # Black bat cutouts
    rng = np.random.default_rng(abs(int(cx * 13 + cy * 7)) % (2**31))
    for _ in range(n_bats):
        dist = rng.uniform(0, moon_r * 0.60)
        ang = rng.uniform(0, 2 * np.pi)
        bx = cx + dist * np.cos(ang)
        by = cy + dist * np.sin(ang)
        bs = moon_r * rng.uniform(0.18, 0.34)
        b_angle_deg = rng.uniform(-20, 20)
        pts = bat_poly_pts(0, 0, bs)
        c, s_ = np.cos(np.radians(b_angle_deg)), np.sin(np.radians(b_angle_deg))
        R = np.array([[c, -s_],[s_, c]])
        pts = (R @ pts.T).T + [bx, by]
        ax.add_patch(Polygon(pts, closed=True, facecolor="black", edgecolor="none", zorder=3))


def draw():
    """4×4 moon tiles with bat negative-space cutouts. Black background, moons staggered."""
    fig, ax = setup_ax()
    cols, rows = 4, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    moon_r = min(dx, dy) * 0.44
    n_bat_options = [2, 3, 4, 5]
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            n_bats = n_bat_options[(row * cols + col) % 4]
            for ox, oy in WRAPS:
                moon_bat_cutout(ax, cx + ox, cy + oy, moon_r, n_bats)
    save(fig, "abstract halloween variation bat moon negative space cutout disc pattern black white texture")


if __name__ == "__main__":
    draw()
