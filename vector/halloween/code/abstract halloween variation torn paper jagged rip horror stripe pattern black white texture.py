import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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


def jagged_edge(rng, y_base, n_teeth, x_start, x_end, amplitude, jag_sharpness=0.5):
    """Generate a jagged torn-paper edge as a list of (x,y) points."""
    xs = np.linspace(x_start, x_end, n_teeth * 2 + 1)
    pts = []
    for i, x in enumerate(xs):
        if i % 2 == 0:
            pts.append((x, y_base))
        else:
            # sharp spike
            spike = rng.uniform(amplitude * 0.4, amplitude) * rng.choice([-1, 1])
            pts.append((x + rng.uniform(-0.5, 0.5), y_base + spike))
    return pts


def draw():
    """Abstract horror rip pattern — alternating white and black horizontal bands
    separated by jagged torn-paper edges, creating a shredded layered effect."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(77)

    # stripe heights (seamless: stripes repeat over PERIOD)
    stripe_h = PERIOD / 5
    n_stripes = 6   # one extra for wrap

    for s in range(n_stripes):
        y_bot = s * stripe_h - stripe_h
        y_top = y_bot + stripe_h
        fill = "white" if s % 2 == 0 else "black"

        for ox, oy in WRAPS:
            # top edge: jagged
            top_edge = jagged_edge(rng, y_top + oy, 28, -2 + ox, PERIOD + 2 + ox,
                                   amplitude=rng.uniform(1.2, 3.0))
            # bottom edge: jagged
            bot_edge = jagged_edge(rng, y_bot + oy, 28, -2 + ox, PERIOD + 2 + ox,
                                   amplitude=rng.uniform(1.2, 3.0))

            pts = top_edge + bot_edge[::-1]
            ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor="none"))

    save(fig, "abstract halloween variation torn paper jagged rip horror stripe pattern black white texture")


if __name__ == "__main__":
    draw()
