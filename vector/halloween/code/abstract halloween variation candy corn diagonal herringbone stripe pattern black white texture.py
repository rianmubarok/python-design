import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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


def candy_corn_shape(ax, cx, cy, length, angle, fill="black", mid_fill="#555"):
    """Single candy corn pointing at `angle`."""
    offset = length * 0.08
    sx = cx + offset * np.cos(angle)
    sy = cy + offset * np.sin(angle)
    eff   = length - offset
    w_base = eff * 0.38
    w_mid  = eff * 0.24
    tip_x  = sx + eff * np.cos(angle)
    tip_y  = sy + eff * np.sin(angle)
    perp   = angle + np.pi / 2

    def side(px, py, hw):
        return [(px + hw * np.cos(perp), py + hw * np.sin(perp)),
                (px - hw * np.cos(perp), py - hw * np.sin(perp))]

    bcx = sx + eff * 0.35 * np.cos(angle)
    bcy = sy + eff * 0.35 * np.sin(angle)
    mcx = sx + eff * 0.70 * np.cos(angle)
    mcy = sy + eff * 0.70 * np.sin(angle)

    base_pts = side(sx, sy, w_base*0.5) + list(reversed(side(bcx, bcy, w_base*0.5)))
    mid_pts  = side(bcx, bcy, w_base*0.5) + list(reversed(side(mcx, mcy, w_mid*0.5)))
    tip_pts  = side(mcx, mcy, w_mid*0.5) + [(tip_x, tip_y)]

    for pts, fc in [(base_pts, fill), (mid_pts, mid_fill), (tip_pts, fill)]:
        ax.add_patch(Polygon(pts, closed=True, facecolor=fc, edgecolor="none"))


def draw():
    """Herringbone diagonal stripe pattern using candy corn shapes.
    Each row of shapes alternates direction: odd rows point +45°, even rows -45°.
    Creates a classic chevron/herringbone weave with Halloween candy corn motif.
    White background, black corn.
    """
    fig, ax = setup_ax()

    cols   = 8
    rows   = 10
    dx     = PERIOD / cols
    dy     = PERIOD / rows
    length = max(dx, dy) * 0.80

    for row in range(rows):
        # Herringbone: alternate +45 / -45 per row
        angle = np.radians(45) if row % 2 == 0 else np.radians(-45)
        shift = dx * 0.5 if (row // 2) % 2 else 0.0   # brick offset every 2 rows
        for col in range(cols):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                candy_corn_shape(ax, cx + ox, cy + oy, length, angle)

    save(fig,
         "abstract halloween variation candy corn diagonal herringbone "
         "stripe pattern black white texture")


if __name__ == "__main__":
    draw()
