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


def draw_crescent(ax, cx, cy, r_outer, tilt, color="white"):
    """Standard crescent silhouette."""
    n = 180
    offset_dist = r_outer * 0.42
    theta_out = np.linspace(-np.pi * 0.60, np.pi * 0.60, n)
    ox = cx + r_outer * np.cos(theta_out)
    oy = cy + r_outer * np.sin(theta_out)

    punch_cx = cx + offset_dist
    punch_cy = cy
    p1 = (ox[-1] - punch_cx, oy[-1] - punch_cy)
    p2 = (ox[0]  - punch_cx, oy[0]  - punch_cy)
    a1 = np.arctan2(p1[1], p1[0])
    a2 = np.arctan2(p2[1], p2[0])
    r_in = np.hypot(p1[0], p1[1])
    theta_in = np.linspace(a1, a2, n)
    ix = punch_cx + r_in * np.cos(theta_in)
    iy = punch_cy + r_in * np.sin(theta_in)

    pts_x = np.concatenate([ox, ix]) - cx
    pts_y = np.concatenate([oy, iy]) - cy
    rot_x = pts_x * np.cos(tilt) - pts_y * np.sin(tilt) + cx
    rot_y = pts_x * np.sin(tilt) + pts_y * np.cos(tilt) + cy
    ax.add_patch(Polygon(np.column_stack([rot_x, rot_y]),
                         closed=True, facecolor=color, edgecolor="none", zorder=2))


def draw_bat_wings_arc(ax, cx, cy, w, h, fill="white"):
    """Bat silhouette where the wing arcs are shaped like crescent arcs —
    the upper wing edge follows a concave crescent curve giving a moon-wing hybrid."""
    # Left wing arc (crescent-style concave top)
    t_out_l = np.linspace(np.pi, np.pi * 1.6, 40)
    t_in_l  = np.linspace(np.pi * 1.5, np.pi * 1.05, 30)
    r_out = w * 0.46
    r_in  = w * 0.28
    # outer arc (upper wing edge)
    xl_out = cx + r_out * np.cos(t_out_l)
    yl_out = cy + h * 0.10 + r_out * 0.65 * np.sin(t_out_l)
    # inner arc (lower wing edge, tighter)
    xl_in  = cx + r_in  * np.cos(t_in_l)
    yl_in  = cy - h * 0.05 + r_in  * 0.55 * np.sin(t_in_l)

    # Right wing (mirror)
    t_out_r = np.linspace(0, -np.pi * 0.6, 40)
    t_in_r  = np.linspace(-np.pi * 0.5, -np.pi * 0.05, 30)
    xr_out = cx + r_out * np.cos(t_out_r)
    yr_out = cy + h * 0.10 + r_out * 0.65 * np.sin(t_out_r)
    xr_in  = cx + r_in  * np.cos(t_in_r)
    yr_in  = cy - h * 0.05 + r_in * 0.55 * np.sin(t_in_r)

    # Left wing polygon
    lpts = np.column_stack([np.concatenate([xl_out, xl_in]),
                            np.concatenate([yl_out, yl_in])])
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(lpts) - 2) + [MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(lpts, codes), facecolor=fill, edgecolor="none", zorder=2))

    # Right wing polygon
    rpts = np.column_stack([np.concatenate([xr_out, xr_in]),
                            np.concatenate([yr_out, yr_in])])
    ax.add_patch(PathPatch(MPath(rpts, codes[:len(rpts)]), facecolor=fill, edgecolor="none", zorder=2))

    # Body (small ellipse)
    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse((cx, cy), w * 0.12, h * 0.30,
                         facecolor=fill, edgecolor="none", zorder=3))
    # Head
    ax.add_patch(Circle((cx, cy + h * 0.18), w * 0.065,
                        facecolor=fill, edgecolor="none", zorder=3))


def draw():
    """3×4 staggered grid. Each cell has:
    - A crescent moon (tilted, medium size)
    - A bat whose wings echo crescent arc shapes, placed just below the moon.
    Alternating tilt direction per row. White on black."""
    fig, ax = setup_ax()

    cols, rows = 3, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    r_moon = min(dx, dy) * 0.22
    bw = dx * 0.56
    bh = dy * 0.38

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        tilt = np.radians(25) if row % 2 == 0 else np.radians(-25)
        for col in range(-1, cols + 2):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    # Crescent sits upper portion of cell
                    draw_crescent(ax, px, py + dy * 0.18, r_moon, tilt)
                    # Bat with arc wings sits just below moon
                    draw_bat_wings_arc(ax, px, py - dy * 0.08, bw, bh)

    save(fig, "abstract halloween variation crescent moon bat wing arc combo paired tile pattern black white texture")


if __name__ == "__main__":
    draw()
