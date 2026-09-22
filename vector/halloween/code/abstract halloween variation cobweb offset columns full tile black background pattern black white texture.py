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


def full_web(ax, cx, cy, max_r, n_spokes=14, n_rings=16,
             col="white", lw_spoke=0.55, lw_ring=0.42):
    """Full radial spider web centred at (cx, cy)."""
    angles = np.linspace(0, 2 * np.pi, n_spokes, endpoint=False)
    ring_radii = np.linspace(max_r * 0.06, max_r, n_rings)

    for a in angles:
        ax.plot([cx, cx + max_r * np.cos(a)],
                [cy, cy + max_r * np.sin(a)],
                color=col, linewidth=lw_spoke, solid_capstyle="round")

    for r in ring_radii:
        pts = np.array([[cx + r * np.cos(a), cy + r * np.sin(a)]
                        for a in angles])
        pts = np.vstack([pts, pts[0]])
        ax.plot(pts[:, 0], pts[:, 1], color=col, linewidth=lw_ring)

    ax.add_patch(Circle((cx, cy), max_r * 0.020,
                        facecolor=col, edgecolor="none"))


def draw():
    """Large full webs on black: 3 columns, odd rows offset by half column width.
    Two web sizes alternate (large / slightly smaller) for depth variation.
    Every web fills its tile edge-to-edge, so rings interlock at tile seams."""
    fig, ax = setup_ax()

    cols = 3
    rows = 4
    dx = PERIOD / cols
    dy = PERIOD / rows

    for row in range(-1, rows + 1):
        for col in range(-1, cols + 1):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            # alternate two sizes
            max_r = (dx if (row + col) % 2 == 0 else dx * 0.78) * 0.58
            n_sp = 16 if (row + col) % 2 == 0 else 12
            for ox, oy in WRAPS:
                full_web(ax, cx + ox, cy + oy, max_r,
                         n_spokes=n_sp, n_rings=14)

    save(fig, "abstract halloween variation cobweb offset columns full tile black background pattern black white texture")


if __name__ == "__main__":
    draw()
