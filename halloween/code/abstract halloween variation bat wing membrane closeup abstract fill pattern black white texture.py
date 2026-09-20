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
    print(f"Saved: {jpg_path}")


def wing_tile(ax, x0, y0, w, h, rng):
    """Bat wing membrane section — abstract organic polygonal cells like stretched skin."""
    # Seed anchor points for a Voronoi-like organic mesh
    n_pts = rng.integers(8, 14)
    pts_x = rng.uniform(x0 + w*0.05, x0 + w*0.95, n_pts)
    pts_y = rng.uniform(y0 + h*0.05, y0 + h*0.95, n_pts)
    # radial bone lines from left edge (wing root) to each anchor
    root_x = x0
    root_y = y0 + h/2
    for i in range(n_pts):
        ax.plot([root_x, pts_x[i]], [root_y, pts_y[i]],
                color="white", linewidth=rng.uniform(0.4, 1.0),
                solid_capstyle="round", alpha=0.7)
    # connect neighbouring anchors
    for i in range(n_pts):
        for j in range(i+1, n_pts):
            dist = np.hypot(pts_x[i]-pts_x[j], pts_y[i]-pts_y[j])
            if dist < w * 0.35:
                ax.plot([pts_x[i],pts_x[j]], [pts_y[i],pts_y[j]],
                        color="white", linewidth=0.35, alpha=0.45)
    # outer membrane edge — wavy top+bottom silhouette
    edge_pts = [(x0, root_y)]
    for t in np.linspace(0, 1, 20):
        ex = x0 + t * w
        ey_top = y0 + h*0.95 + rng.uniform(-h*0.04, h*0.04)
        edge_pts.append((ex, ey_top))
    for t in np.linspace(1, 0, 20):
        ex = x0 + t * w
        ey_bot = y0 + h*0.05 + rng.uniform(-h*0.04, h*0.04)
        edge_pts.append((ex, ey_bot))
    ax.add_patch(Polygon(edge_pts, closed=True, facecolor="none",
                         edgecolor="white", linewidth=0.6, alpha=0.5))


def draw():
    """3×3 bat wing membrane tiles — each tile is one abstract wing section."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(14)
    cols, rows = 3, 3
    dx, dy = PERIOD/cols, PERIOD/rows
    for row in range(rows):
        for col in range(cols):
            x0 = col*dx; y0 = row*dy
            for ox, oy in WRAPS:
                wing_tile(ax, x0+ox, y0+oy, dx, dy, rng)
    save(fig, "abstract halloween variation bat wing membrane closeup abstract fill pattern black white texture")


if __name__ == "__main__":
    draw()
