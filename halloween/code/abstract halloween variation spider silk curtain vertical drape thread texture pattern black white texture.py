import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
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


def silk_curtain(ax, x_anchor, y_top, rng):
    """Vertical silk thread that sways and has horizontal connecting strands."""
    n_pts = 80
    # main vertical thread with gentle sine sway
    sway_freq = rng.uniform(0.8, 2.0)
    sway_amp = rng.uniform(0.3, 1.2)
    ys = np.linspace(y_top, y_top - PERIOD * 1.05, n_pts)
    xs = x_anchor + sway_amp * np.sin(ys * sway_freq * 0.22)
    lw = rng.uniform(0.5, 1.0)
    for ox, oy in WRAPS:
        ax.plot(xs + ox, ys + oy, color="white", linewidth=lw, alpha=0.82,
                solid_capstyle="round")


def draw():
    """Dense vertical silk curtain — 30 draping threads with horizontal connecting strands."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(61)
    n_threads = 30
    xs = sorted(rng.uniform(0, PERIOD, n_threads))

    for x in xs:
        silk_curtain(ax, x, PERIOD + 2, rng)

    # horizontal connecting strands at intervals
    n_h_strands = 22
    ys_h = rng.uniform(2, PERIOD - 2, n_h_strands)
    for y in ys_h:
        # wavy horizontal strand
        xpts = np.linspace(-2, PERIOD + 2, 200)
        ypts = y + rng.uniform(0.2, 0.8) * np.sin(xpts * rng.uniform(0.15, 0.45))
        for ox, oy in WRAPS:
            ax.plot(xpts + ox, ypts + oy, color="white",
                    linewidth=rng.uniform(0.3, 0.6), alpha=0.55)

    save(fig, "abstract halloween variation spider silk curtain vertical drape thread texture pattern black white texture")


if __name__ == "__main__":
    draw()
