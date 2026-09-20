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
    ax.set_facecolor("white")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Saved: {jpg_path}")


def shattered_web(ax, cx, cy, r, rng):
    """Spider web where rings are broken/shattered — segments offset & missing."""
    spokes = 10
    angles = [k * 2 * np.pi / spokes for k in range(spokes)]

    # draw spokes with random gaps / offset displacement
    for a in angles:
        # shatter: break spoke into 2-3 segments with kinks
        break_t = rng.uniform(0.3, 0.7)
        kink_angle = rng.uniform(-0.18, 0.18)
        bx = cx + r * break_t * np.cos(a + kink_angle)
        by = cy + r * break_t * np.sin(a + kink_angle)
        ex = cx + r * np.cos(a)
        ey = cy + r * np.sin(a)
        ax.plot([cx, bx], [cy, by], color="black", linewidth=0.7, solid_capstyle="round")
        if rng.random() > 0.15:   # sometimes the outer segment is missing
            ax.plot([bx, ex], [by, ey], color="black", linewidth=0.7, solid_capstyle="round")

    # draw concentric rings with broken/shifted segments
    for sc in (0.22, 0.40, 0.60, 0.82):
        ring_pts = [(cx + r * sc * np.cos(a), cy + r * sc * np.sin(a)) for a in angles]
        # draw arc-by-arc, randomly skipping or offsetting
        for i in range(spokes):
            if rng.random() < 0.18:  # skip this segment (crack)
                continue
            p1 = np.array(ring_pts[i])
            p2 = np.array(ring_pts[(i + 1) % spokes])
            # offset the midpoint for shatter distortion
            mid = (p1 + p2) / 2 + rng.uniform(-r * 0.04, r * 0.04, 2)
            ax.plot([p1[0], mid[0], p2[0]], [p1[1], mid[1], p2[1]],
                    color="black", linewidth=0.55)

    # impact point crack lines radiating outward past the web
    n_cracks = rng.integers(3, 7)
    for _ in range(n_cracks):
        ca = rng.uniform(0, 2 * np.pi)
        crack_len = r * rng.uniform(0.3, 0.6)
        bx = cx + r * rng.uniform(0.1, 0.4) * np.cos(ca)
        by = cy + r * rng.uniform(0.1, 0.4) * np.sin(ca)
        ex = cx + (r + crack_len) * np.cos(ca)
        ey = cy + (r + crack_len) * np.sin(ca)
        ax.plot([bx, ex], [by, ey], color="black", linewidth=0.9, solid_capstyle="round")

    # impact centre dot
    ax.add_patch(Circle((cx, cy), r * 0.04, facecolor="black", edgecolor="none"))


def draw():
    """Shattered/fractured spider web field — non-uniform webs with cracks, gaps and
    impact radiants. Staggered 6×6 layout for a broken-glass aesthetic."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(99)
    cols, rows = 6, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    r = min(dx, dy) * 0.60
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                shattered_web(ax, cx + ox, cy + oy, r, rng)
    save(fig, "abstract halloween variation fractured spiderweb shattered glass distortion pattern black white texture")


if __name__ == "__main__":
    draw()
