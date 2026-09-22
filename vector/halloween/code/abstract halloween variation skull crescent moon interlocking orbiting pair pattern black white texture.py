import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon
from matplotlib.transforms import Affine2D
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI  = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR  = SCRIPT_DIR.parent / "output"
JPG_DIR     = OUTPUT_DIR / "jpg"
SVG_DIR     = OUTPUT_DIR / "svg"
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


def draw_crescent(ax, cx, cy, r_outer, tilt, fill="white"):
    n_pts = 160
    offset_dist = r_outer * 0.42
    theta_outer = np.linspace(-np.pi * 0.58, np.pi * 0.58, n_pts)
    outer_x = cx + r_outer * np.cos(theta_outer)
    outer_y = cy + r_outer * np.sin(theta_outer)
    punch_cx, punch_cy = cx + offset_dist, cy
    p1 = (outer_x[-1] - punch_cx, outer_y[-1] - punch_cy)
    p2 = (outer_x[0]  - punch_cx, outer_y[0]  - punch_cy)
    a1, a2 = np.arctan2(p1[1], p1[0]), np.arctan2(p2[1], p2[0])
    r_in = np.hypot(p1[0], p1[1])
    inner_x = punch_cx + r_in * np.cos(np.linspace(a1, a2, n_pts))
    inner_y = punch_cy + r_in * np.sin(np.linspace(a1, a2, n_pts))
    pts_x = np.concatenate([outer_x, inner_x]) - cx
    pts_y = np.concatenate([outer_y, inner_y]) - cy
    rx = pts_x * np.cos(tilt) - pts_y * np.sin(tilt) + cx
    ry = pts_x * np.sin(tilt) + pts_y * np.cos(tilt) + cy
    ax.add_patch(Polygon(np.column_stack([rx, ry]),
                         closed=True, facecolor=fill, edgecolor="none"))


def draw_skull_small(ax, cx, cy, s):
    """Compact skull without crossbones — white on black."""
    ax.add_patch(Ellipse((cx, cy + 0.10 * s), 0.68 * s, 0.58 * s,
                         facecolor="white", edgecolor="none"))
    ax.add_patch(FancyBboxPatch(
        (cx - 0.20 * s, cy - 0.16 * s), 0.40 * s, 0.15 * s,
        boxstyle=f"round,pad=0,rounding_size={0.030*s:.4f}",
        facecolor="white", edgecolor="none"))
    for ex in (-0.14 * s, 0.14 * s):
        ax.add_patch(Ellipse((cx + ex, cy + 0.14 * s), 0.14 * s, 0.15 * s,
                             facecolor="black", edgecolor="none"))
    ax.add_patch(Polygon(
        np.array([[cx, cy + 0.02 * s],
                  [cx - 0.04*s, cy - 0.06 * s],
                  [cx + 0.04*s, cy - 0.06 * s]]),
        closed=True, facecolor="black", edgecolor="none"))


def draw_tile(ax, cx, cy, r):
    """One tile: crescent moon hugging a skull.
    The skull sits at the tile centre; crescent arcs around it top-right.
    """
    skull_s = r * 0.60
    # Large crescent behind/around skull, tilted ~135° (opening faces skull)
    draw_crescent(ax, cx + r * 0.18, cy + r * 0.10, r * 0.92,
                  tilt=np.radians(135), fill="white")
    # Draw skull on top
    draw_skull_small(ax, cx, cy, skull_s)


def draw():
    """3×4 grid of skull + crescent moon interlocking pair tiles.
    Staggered rows. Black background.
    """
    fig, ax = setup_ax()
    cols, rows = 3, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    r = min(dx, dy) * 0.40

    for row in range(rows):
        shift = dx * 0.5 if row % 2 else 0.0
        for col in range(cols):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                draw_tile(ax, cx + ox, cy + oy, r)

    save(fig,
         "abstract halloween variation skull crescent moon interlocking "
         "orbiting pair pattern black white texture")


if __name__ == "__main__":
    draw()
