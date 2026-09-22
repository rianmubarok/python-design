import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse, FancyBboxPatch, Polygon, Circle
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


def draw_pumpkin(ax, cx, cy, s, angle=0.0, fill="white"):
    """Pumpkin rotated by `angle` radians around its centre."""
    inv = "black" if fill == "white" else "white"

    def rot(x, y):
        rx = (x - cx) * np.cos(angle) - (y - cy) * np.sin(angle) + cx
        ry = (x - cx) * np.sin(angle) + (y - cy) * np.cos(angle) + cy
        return rx, ry

    # Three lobes
    for ddx in (-s * 0.22, 0.0, s * 0.22):
        t = np.linspace(0, 2 * np.pi, 60)
        lx = cx + ddx + s * 0.28 * np.cos(t)
        ly = cy + s * 0.44 * np.sin(t)
        rx, ry = rot(lx, ly)
        ax.add_patch(Polygon(np.column_stack([rx, ry]),
                             closed=True, facecolor=fill, edgecolor="none"))

    # Stem
    sx0 = cx - s * 0.035; sy0 = cy + s * 0.22
    stem_pts_x = [sx0, sx0, sx0 + s * 0.07, sx0 + s * 0.07]
    stem_pts_y = [sy0, sy0 + s * 0.14, sy0 + s * 0.14, sy0]
    srx, sry = rot(np.array(stem_pts_x), np.array(stem_pts_y))
    ax.add_patch(Polygon(np.column_stack([srx, sry]),
                         closed=True, facecolor=fill, edgecolor="none"))

    # Triangle eyes
    for ex in (-s * 0.13, s * 0.13):
        epts = np.array([
            [cx + ex, cy + s * 0.11],
            [cx + ex - s * 0.065, cy - s * 0.02],
            [cx + ex + s * 0.065, cy - s * 0.02],
        ])
        rx2, ry2 = rot(epts[:, 0], epts[:, 1])
        ax.add_patch(Polygon(np.column_stack([rx2, ry2]),
                             closed=True, facecolor=inv, edgecolor="none"))

    # Mouth zig-zag
    x_m = np.array([-0.15, -0.09, -0.03, 0.03, 0.09, 0.15]) * s + cx
    y_m = np.array([-0.13, -0.06, -0.13, -0.06, -0.13, -0.06]) * s + cy
    # Close below
    x_close = np.array([0.15, 0.15, -0.15, -0.15]) * s + cx
    y_close = np.array([-0.06, -0.17, -0.17, -0.13]) * s + cy
    mx = np.concatenate([x_m, x_close])
    my = np.concatenate([y_m, y_close])
    rx3, ry3 = rot(mx, my)
    pts = np.column_stack([rx3, ry3])
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 2) + [MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(pts, codes), facecolor=inv, edgecolor="none"))


def radial_ring(ax, hub_cx, hub_cy, n, orbit_r, pumpkin_s, angle_offset=0.0):
    """Place n pumpkins radially around hub, each facing outward."""
    for k in range(n):
        a = angle_offset + k * 2 * np.pi / n
        px = hub_cx + orbit_r * np.cos(a)
        py = hub_cy + orbit_r * np.sin(a)
        draw_pumpkin(ax, px, py, pumpkin_s, angle=a + np.pi / 2)


def draw():
    """2×2 tile of sunburst pumpkin rings. Each tile has:
    - Centre pumpkin (upright)
    - Inner ring of 6 pumpkins facing outward
    - Outer ring of 10 pumpkins facing outward
    Tiled seamlessly at PERIOD."""
    fig, ax = setup_ax()

    cols, rows = 2, 2
    dx, dy = PERIOD / cols, PERIOD / rows
    hub_s = dy * 0.14

    for row in range(-1, rows + 1):
        for col in range(-1, cols + 1):
            hx = (col + 0.5) * dx
            hy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = hx + ox, hy + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    # Centre
                    draw_pumpkin(ax, px, py, hub_s * 0.90, angle=0.0)
                    # Inner ring
                    radial_ring(ax, px, py, 6, dx * 0.22, hub_s * 0.65, angle_offset=0.0)
                    # Outer ring
                    radial_ring(ax, px, py, 10, dx * 0.40, hub_s * 0.50, angle_offset=np.radians(18))

    save(fig, "abstract halloween variation pumpkin radial spiral sunburst arrangement pattern black white texture")


if __name__ == "__main__":
    draw()
