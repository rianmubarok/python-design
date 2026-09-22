import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon, Rectangle
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
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
    print(f"Saved: {jpg_path} | {svg_path}")


def skull(ax, cx, cy, s, fill="black"):
    inv = "white" if fill == "black" else "black"
    # No edge on any part — jaw box artifact removed by using a Polygon jaw instead.
    skull_cy = cy + 0.08 * s

    # Cranium ellipse — no outline at all (black variant: fill; white variant: fill only)
    edge = "none"
    ax.add_patch(Ellipse((cx, skull_cy + 0.09 * s), 0.72 * s, 0.62 * s,
                         facecolor=fill, edgecolor=edge, linewidth=0))

    # Jaw — drawn as a rounded Polygon so no FancyBboxPatch outline artifact.
    # Build a rounded-rect polygon manually via arc corners.
    jx0 = cx - 0.22 * s
    jy0 = skull_cy - 0.22 * s
    jw  = 0.44 * s
    jh  = 0.18 * s
    r   = 0.035 * s   # corner radius
    # 4 rounded corners
    jaw_pts = []
    for (ox2, oy2, a_start, a_end) in [
        (jx0 + r,      jy0 + r,      np.pi,       1.5*np.pi),
        (jx0 + jw - r, jy0 + r,      1.5*np.pi,   2*np.pi  ),
        (jx0 + jw - r, jy0 + jh - r, 0,           0.5*np.pi),
        (jx0 + r,      jy0 + jh - r, 0.5*np.pi,   np.pi    ),
    ]:
        t = np.linspace(a_start, a_end, 8)
        jaw_pts.extend(zip(ox2 + r * np.cos(t), oy2 + r * np.sin(t)))
    ax.add_patch(Polygon(jaw_pts, closed=True, facecolor=fill, edgecolor="none", linewidth=0))

    # Eye sockets
    for ex in (-0.155 * s, 0.155 * s):
        ax.add_patch(Ellipse((cx + ex, skull_cy + 0.13 * s),
                             0.165 * s, 0.185 * s,
                             facecolor=inv, edgecolor="none"))
    # Nose cavity
    ax.add_patch(Polygon(
        [[cx, skull_cy + 0.01 * s],
         [cx - 0.055 * s, skull_cy - 0.075 * s],
         [cx + 0.055 * s, skull_cy - 0.075 * s]],
        closed=True, facecolor=inv, edgecolor="none"))
    # Teeth — use Polygon to avoid any box outline
    for tx in (-0.095 * s, 0.0, 0.095 * s):
        tx0 = cx + tx - 0.022 * s
        ty0 = skull_cy - 0.195 * s
        tw  = 0.044 * s
        th  = 0.085 * s
        tr  = 0.008 * s
        tooth_pts = []
        for (ox2, oy2, a_start, a_end) in [
            (tx0 + tr,      ty0 + tr,      np.pi,       1.5*np.pi),
            (tx0 + tw - tr, ty0 + tr,      1.5*np.pi,   2*np.pi  ),
            (tx0 + tw - tr, ty0 + th - tr, 0,           0.5*np.pi),
            (tx0 + tr,      ty0 + th - tr, 0.5*np.pi,   np.pi    ),
        ]:
            t = np.linspace(a_start, a_end, 6)
            tooth_pts.extend(zip(ox2 + tr * np.cos(t), oy2 + tr * np.sin(t)))
        ax.add_patch(Polygon(tooth_pts, closed=True, facecolor=inv, edgecolor="none", linewidth=0))


def draw():
    """Skulls on a regular 6×6 grid; diagonal band stripes alternate black and white fills.
    Band index = floor((col - row + n) % stripe_period) determines fill colour.
    The diagonal stripe period is 2 cells so the pattern is black/white/black/white…
    seamless tile."""
    fig, ax = setup_ax()

    cols, rows = 6, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.72

    for row in range(-1, rows + 1):
        for col in range(-1, cols + 1):
            # Diagonal stripe: use (col - row) mod 2 for clean alternation
            fill = "black" if (col - row) % 2 == 0 else "white"
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    skull(ax, px, py, s, fill=fill)

    save(fig, "abstract halloween variation skull diagonal band stripe fill alternating pattern black white texture")


if __name__ == "__main__":
    draw()
