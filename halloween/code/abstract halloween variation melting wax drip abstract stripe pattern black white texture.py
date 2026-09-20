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


def wax_drip_column(ax, x_center, top_y, base_width, rng):
    """A full vertical wax drip column from top_y downward, with bulging drips."""
    # main column shaft (thin)
    shaft_w = base_width * rng.uniform(0.18, 0.30)
    col_height = PERIOD * 1.05
    # shaft as a slightly wavy polygon
    n = 60
    ys = np.linspace(top_y, top_y - col_height, n)
    left_xs = x_center - shaft_w/2 + rng.uniform(-0.15, 0.15, n)
    right_xs = x_center + shaft_w/2 + rng.uniform(-0.15, 0.15, n)
    shaft_pts = list(zip(left_xs, ys)) + list(zip(right_xs[::-1], ys[::-1]))
    ax.add_patch(Polygon(shaft_pts, closed=True, facecolor="white", edgecolor="none"))

    # drip bulges at random positions along shaft
    n_drips = rng.integers(3, 7)
    drip_ys = rng.uniform(top_y - col_height * 0.92, top_y - col_height * 0.10, n_drips)
    for dy_ in drip_ys:
        dr = rng.uniform(base_width * 0.25, base_width * 0.55)
        tail_h = rng.uniform(base_width * 0.4, base_width * 1.0)
        # bulge circle
        ax.add_patch(Circle((x_center, dy_ - dr * 0.6), dr,
                            facecolor="white", edgecolor="none"))
        # tail above the bulge
        pts = [
            (x_center - shaft_w/2, dy_ + tail_h),
            (x_center - dr * 0.5, dy_ - dr * 0.1),
            (x_center + dr * 0.5, dy_ - dr * 0.1),
            (x_center + shaft_w/2, dy_ + tail_h),
        ]
        ax.add_patch(Polygon(pts, closed=True, facecolor="white", edgecolor="none"))


def draw():
    """Vertical wax drip columns of varying widths — purely abstract, no candle.
    Columns are seamless top-to-bottom. Dense irregular spacing across x."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(66)
    # place columns at irregular x positions
    n_cols = 18
    xs = sorted(rng.uniform(2, PERIOD - 2, n_cols))
    for x in xs:
        bw = rng.uniform(2.5, 6.0)
        for ox, oy in WRAPS:
            wax_drip_column(ax, x + ox, PERIOD + 2 + oy, bw, rng)
    save(fig, "abstract halloween variation melting wax drip abstract stripe pattern black white texture")


if __name__ == "__main__":
    draw()
