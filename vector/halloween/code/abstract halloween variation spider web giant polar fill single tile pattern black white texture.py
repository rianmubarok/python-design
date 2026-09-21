import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
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


def giant_web(ax, cx, cy, max_r, n_spokes=16, n_rings=18):
    """A single large polar-coordinate spider web centred at (cx,cy)."""
    angles = [k * 2 * np.pi / n_spokes for k in range(n_spokes)]
    ring_radii = np.linspace(max_r * 0.06, max_r, n_rings)

    # draw spokes
    for a in angles:
        ax.plot([cx, cx + max_r * np.cos(a)],
                [cy, cy + max_r * np.sin(a)],
                color="white", linewidth=0.7, solid_capstyle="round")

    # draw spiral-ish concentric rings (each ring has slightly increasing spacing)
    for r in ring_radii:
        pts = np.array([[cx + r * np.cos(a), cy + r * np.sin(a)] for a in angles])
        pts = np.vstack([pts, pts[0]])
        ax.plot(pts[:, 0], pts[:, 1], color="white", linewidth=0.55)

    # centre dot (spider hole)
    ax.add_patch(Circle((cx, cy), max_r * 0.025, facecolor="white", edgecolor="none"))


def draw():
    """3×3 tiles, each completely filled with a single large polar spider web.
    The web extends edge to edge — centre offset on alternate tiles for variety."""
    fig, ax = setup_ax()
    cols, rows = 3, 3
    dx, dy = PERIOD / cols, PERIOD / rows
    r = min(dx, dy) * 0.76
    offsets = [(0, 0), (0.3, 0.2), (-0.2, 0.3),
               (0.1, -0.25), (0, 0), (0.25, 0.1),
               (-0.15, 0.2), (0.2, -0.15), (0, 0)]
    idx = 0
    for row in range(rows):
        for col in range(cols):
            base_cx = (col + 0.5) * dx
            base_cy = (row + 0.5) * dy
            ox_off, oy_off = offsets[idx % len(offsets)]
            cx = base_cx + ox_off * dx
            cy = base_cy + oy_off * dy
            n_spokes = 14 if idx % 2 == 0 else 18
            for ox, oy in WRAPS:
                giant_web(ax, cx + ox, cy + oy, r, n_spokes=n_spokes)
            idx += 1
    save(fig, "abstract halloween variation spider web giant polar fill single tile pattern black white texture")


if __name__ == "__main__":
    draw()
