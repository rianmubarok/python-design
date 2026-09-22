import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Circle
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
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
    print(f"Saved: {jpg_path} | {svg_path}")


def draw_crescent(ax, cx, cy, r_outer, tilt, fill="black"):
    n = 160
    od = r_outer * 0.42
    theta_o = np.linspace(-np.pi * 0.58, np.pi * 0.58, n)
    ox_ = cx + r_outer * np.cos(theta_o)
    oy_ = cy + r_outer * np.sin(theta_o)
    pcx, pcy = cx + od, cy
    p1 = (ox_[-1] - pcx, oy_[-1] - pcy)
    p2 = (ox_[0]  - pcx, oy_[0]  - pcy)
    a1, a2 = np.arctan2(p1[1], p1[0]), np.arctan2(p2[1], p2[0])
    ri = np.hypot(*p1)
    ix_ = pcx + ri * np.cos(np.linspace(a1, a2, n))
    iy_ = pcy + ri * np.sin(np.linspace(a1, a2, n))
    ptx = np.concatenate([ox_, ix_]) - cx
    pty = np.concatenate([oy_, iy_]) - cy
    rx = ptx * np.cos(tilt) - pty * np.sin(tilt) + cx
    ry = ptx * np.sin(tilt) + pty * np.cos(tilt) + cy
    ax.add_patch(Polygon(np.column_stack([rx, ry]),
                         closed=True, facecolor=fill, edgecolor="none"))


def draw_arched_cat(ax, cx, cy, s, fill="black"):
    """Stylised black cat silhouette — arched back, raised tail, pointy ears.
    Pure geometric shapes; no gaps.
    """
    # Body: elongated ellipse arched upward
    body_cx, body_cy = cx + s * 0.05, cy - s * 0.04
    ax.add_patch(Ellipse((body_cx, body_cy), s * 0.90, s * 0.48,
                         facecolor=fill, edgecolor="none", angle=-10))

    # Head: circle, slightly above-right of body
    head_cx, head_cy = cx + s * 0.34, cy + s * 0.12
    head_r = s * 0.20
    ax.add_patch(Circle((head_cx, head_cy), head_r,
                        facecolor=fill, edgecolor="none"))

    # Ears: two small triangles on head
    for side, ear_angle in [(-1, 150), (1, 30)]:
        ea = np.radians(ear_angle)
        etip_x = head_cx + head_r * 0.85 * np.cos(ea)
        etip_y = head_cy + head_r * 0.85 * np.sin(ea)
        ep = ea + np.pi / 2
        base_l = head_r * 0.38
        ear_pts = [
            (head_cx + base_l * np.cos(ep + 0.5), head_cy + base_l * np.sin(ep + 0.5)),
            (etip_x, etip_y),
            (head_cx + base_l * np.cos(ep - 0.5), head_cy + base_l * np.sin(ep - 0.5)),
        ]
        ax.add_patch(Polygon(ear_pts, closed=True, facecolor=fill, edgecolor="none"))

    # Tail: arced strip curling upward to the left
    t_angles = np.linspace(np.radians(-160), np.radians(-30), 40)
    tail_cx, tail_cy = cx - s * 0.42, cy - s * 0.06
    tail_r = s * 0.36
    tail_hw = s * 0.055
    # outer arc
    ox_ = tail_cx + (tail_r + tail_hw) * np.cos(t_angles)
    oy_ = tail_cy + (tail_r + tail_hw) * np.sin(t_angles)
    # inner arc (reversed)
    ix_ = tail_cx + (tail_r - tail_hw) * np.cos(t_angles[::-1])
    iy_ = tail_cy + (tail_r - tail_hw) * np.sin(t_angles[::-1])
    tail_pts = np.column_stack([np.concatenate([ox_, ix_]),
                                np.concatenate([oy_, iy_])])
    ax.add_patch(Polygon(tail_pts, closed=True, facecolor=fill, edgecolor="none"))

    # Small eye (white dot on head)
    ax.add_patch(Circle((head_cx + head_r * 0.22, head_cy + head_r * 0.15),
                        head_r * 0.14, facecolor="white", edgecolor="none"))


def draw_tile(ax, cx, cy, r):
    """Tile: crescent moon in top-left, cat in lower-right, orbiting each other."""
    # Crescent: upper-left, opening toward cat
    draw_crescent(ax, cx - r * 0.28, cy + r * 0.22, r * 0.52,
                  tilt=np.radians(-30), fill="black")
    # Cat: lower-right
    draw_arched_cat(ax, cx + r * 0.10, cy - r * 0.14, r * 0.60, fill="black")


def draw():
    """3×4 grid of black cat + crescent moon orbiting duo tiles.
    White background. Staggered rows.
    """
    fig, ax = setup_ax()
    cols, rows = 3, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    r = min(dx, dy) * 0.46

    for row in range(rows):
        shift = dx * 0.5 if row % 2 else 0.0
        for col in range(cols):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                draw_tile(ax, cx + ox, cy + oy, r)

    save(fig,
         "abstract halloween variation black cat arched crescent moon orbiting "
         "duo pair pattern black white texture")


if __name__ == "__main__":
    draw()
