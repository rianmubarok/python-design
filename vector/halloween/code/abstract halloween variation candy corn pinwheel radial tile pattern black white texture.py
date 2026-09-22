import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
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


def candy_corn(ax, cx, cy, length, angle, fill="white", mid_fill="#888888"):
    """Single candy corn triangle pointing outward at given angle.
    Three colour bands (white base, grey mid-band, white tip)."""
    # Memberikan sedikit offset dari pusat agar tidak menumpuk di tengah
    offset = length * 0.1
    start_x = cx + offset * np.cos(angle)
    start_y = cy + offset * np.sin(angle)

    effective_length = length - offset
    width_base = effective_length * 0.36
    width_mid  = effective_length * 0.22

    tip_x = start_x + effective_length * np.cos(angle)
    tip_y = start_y + effective_length * np.sin(angle)
    perp  = angle + np.pi / 2

    def side(cx_, cy_, half_w):
        return [(cx_ + half_w * np.cos(perp), cy_ + half_w * np.sin(perp)),
                (cx_ - half_w * np.cos(perp), cy_ - half_w * np.sin(perp))]

    # Titik pemisah segmen
    base_cx = start_x + effective_length * 0.35 * np.cos(angle)
    base_cy = start_y + effective_length * 0.35 * np.sin(angle)
    mid_cx  = start_x + effective_length * 0.70 * np.cos(angle)
    mid_cy  = start_y + effective_length * 0.70 * np.sin(angle)

    base_pts = side(start_x, start_y, width_base * 0.5) + list(reversed(side(base_cx, base_cy, width_base * 0.5)))
    mid_pts  = side(base_cx, base_cy, width_base * 0.5) + list(reversed(side(mid_cx, mid_cy, width_mid * 0.5)))
    tip_pts  = side(mid_cx, mid_cy, width_mid * 0.5) + [(tip_x, tip_y)]

    ax.add_patch(Polygon(base_pts, closed=True, facecolor=fill, edgecolor="none"))
    ax.add_patch(Polygon(mid_pts,  closed=True, facecolor=mid_fill, edgecolor="none"))
    ax.add_patch(Polygon(tip_pts,  closed=True, facecolor=fill, edgecolor="none"))


def pinwheel(ax, cx, cy, r, n=6, base_angle=0.0):
    """n candy corns arranged radially like pinwheel spokes."""
    for k in range(n):
        angle = base_angle + k * (2 * np.pi / n)
        candy_corn(ax, cx, cy, r, angle, fill="white", mid_fill="#888888")
    
    # Small hub dot dengan garis tepi rapi di pusat
    ax.add_patch(Circle((cx, cy), r * 0.08, facecolor="white", edgecolor="black", linewidth=1.5))


def draw():
    """4×4 staggered grid, each tile a 6-spoke candy corn pinwheel.
    Alternate tiles have a 30° rotation offset for visual rhythm."""
    fig, ax = setup_ax()
    cols, rows = 4, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    r = min(dx, dy) * 0.42

    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            base_angle = np.radians(30) if (row + col) % 2 else 0.0
            for ox, oy in WRAPS:
                pinwheel(ax, cx + ox, cy + oy, r, n=6, base_angle=base_angle)

    save(fig, "abstract halloween variation candy corn pinwheel radial tile pattern black white texture")


if __name__ == "__main__":
    draw()