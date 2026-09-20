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
EPS_DIR = OUTPUT_DIR / \"eps\"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


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
    eps_path = EPS_DIR / f\"{name} {DATE}.eps\"
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format=\"eps\", pad_inches=0, facecolor=\"white\", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path} | {eps_path}")


def crescent(ax, cx, cy, r, angle_deg=0):
    """Draw a crescent by subtracting an offset circle from a filled circle.
    Crescent orientation controlled by angle_deg."""
    ang = np.radians(angle_deg)
    offset = r * 0.55
    # outer disc
    ax.add_patch(Circle((cx, cy), r, facecolor="white", edgecolor="none", zorder=2))
    # inner cutout shifted in the angle direction
    ax.add_patch(Circle((cx + offset * np.cos(ang), cy + offset * np.sin(ang)),
                        r * 0.80, facecolor="black", edgecolor="none", zorder=3))


def draw():
    """Seamless crescent moon chain — alternating horizontal and vertical crescents
    arranged in a brick-like offset grid, all facing different cardinal directions
    so they visually link into chain-like rows on a black background."""
    fig, ax = setup_ax()
    cols, rows = 10, 10
    dx, dy = PERIOD / cols, PERIOD / rows
    r = min(dx, dy) * 0.48
    directions = [0, 90, 180, 270]   # right, up, left, down
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            # cycle direction based on position
            d = directions[(row * cols + col) % 4]
            for ox, oy in WRAPS:
                crescent(ax, cx + ox, cy + oy, r, angle_deg=d)
    save(fig, "abstract halloween variation crescent moon chain link interlocking pattern black white texture")


if __name__ == "__main__":
    draw()
