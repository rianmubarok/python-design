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
    print(f"Saved: {jpg_path} | {svg_path}")


def bat_poly(cx, cy, s):
    pts = np.array([
        [0.00, 0.08],[0.12,0.18],[0.10,0.05],[0.42,0.22],[0.78,0.38],
        [0.62,0.08],[0.95,0.12],[0.55,-0.08],[0.72,-0.28],[0.28,-0.10],
        [0.18,-0.22],[0.08,-0.08],[0.00,-0.18],
        [-0.08,-0.08],[-0.18,-0.22],[-0.28,-0.10],[-0.72,-0.28],
        [-0.55,-0.08],[-0.95,0.12],[-0.62,0.08],[-0.78,0.38],
        [-0.42,0.22],[-0.10,0.05],[-0.12,0.18],
    ]) * s + [cx, cy]
    return pts


def draw():
    """Bat size gradient — largest bats at tile corners, smallest at centre.
    Uses a 2×2 macro tile repeat with 7×7 internal bat grid."""
    fig, ax = setup_ax()
    tile = PERIOD / 2   # 2 macro tiles across
    n = 7               # bats per macro tile side
    step = tile / n
    max_s = step * 0.46
    min_s = step * 0.12

    for macro_row in range(2):
        for macro_col in range(2):
            mx = macro_col * tile
            my = macro_row * tile
            centre = np.array([mx + tile/2, my + tile/2])
            for row in range(n):
                for col in range(n):
                    cx = mx + (col+0.5)*step
                    cy = my + (row+0.5)*step
                    dist = np.hypot(cx - centre[0], cy - centre[1])
                    max_dist = tile * 0.707
                    frac = dist / max_dist
                    s = min_s + (max_s - min_s) * frac
                    for ox, oy in WRAPS:
                        ax.add_patch(Polygon(bat_poly(cx+ox, cy+oy, s),
                                             closed=True, facecolor="white", edgecolor="none"))
    save(fig, "abstract halloween variation bat size gradient giant corners tiny centre pattern black white texture")


if __name__ == "__main__":
    draw()
