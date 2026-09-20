import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
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


def blood_drop(ax, cx, cy_top, drop_r, tail_len):
    """A teardrop blood drip: rounded bottom bulb + vertical tail."""
    # round bulb at the bottom
    bx, by = cx, cy_top - tail_len
    ax.add_patch(Circle((bx, by), drop_r, facecolor="white", edgecolor="none", zorder=3))
    # tail (tapers from drop_r at bulb top to thin point at top)
    tail_pts = [
        (cx - drop_r * 0.35, by + drop_r * 0.75),
        (cx - 0.5, cy_top + drop_r * 0.3),
        (cx, cy_top),
        (cx + 0.5, cy_top + drop_r * 0.3),
        (cx + drop_r * 0.35, by + drop_r * 0.75),
    ]
    ax.add_patch(Polygon(tail_pts, closed=True, facecolor="white", edgecolor="none", zorder=3))
    # highlight on bulb
    ax.add_patch(Circle((bx - drop_r * 0.28, by + drop_r * 0.28), drop_r * 0.18,
                        facecolor="black", edgecolor="none", zorder=4))


def draw():
    """Dripping blood drops hanging from the top of each tile row —
    a seamless stripe of drops at varying heights on black background."""
    fig, ax = setup_ax()
    np.random.seed(7)
    cols = 14
    dx = PERIOD / cols
    # rows of drip origins at different y levels
    drip_rows = [100.0, 75.0, 50.0, 25.0, 0.0]   # seamless: 0 = 100 wraps
    for drip_y in drip_rows:
        for col in range(cols):
            cx = (col + 0.5) * dx + np.random.uniform(-dx * 0.2, dx * 0.2)
            drop_r = np.random.uniform(2.2, 3.8)
            tail_len = np.random.uniform(3.5, 10.0)
            for ox, oy in WRAPS:
                blood_drop(ax, cx + ox, drip_y + oy, drop_r, tail_len)
    save(fig, "abstract halloween variation dripping blood drop repeating stripe pattern black white texture")


if __name__ == "__main__":
    draw()
