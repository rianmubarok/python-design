import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon
from matplotlib.transforms import Affine2D
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


def skull_micro(ax, cx, cy, s):
    """Ultra-compact skull silhouette – cranium + hint of eye sockets only, white on black."""
    # cranium
    ax.add_patch(Ellipse((cx, cy + 0.12 * s), 0.70 * s, 0.58 * s,
                         facecolor="white", edgecolor="none"))
    # jaw stub
    ax.add_patch(FancyBboxPatch(
        (cx - 0.20 * s, cy - 0.16 * s), 0.40 * s, 0.16 * s,
        boxstyle=f"round,pad=0,rounding_size={0.030*s:.4f}",
        facecolor="white", edgecolor="none"))
    # eye sockets (black cutouts)
    for ex in (-0.145 * s, 0.145 * s):
        ax.add_patch(Ellipse((cx + ex, cy + 0.16 * s), 0.15 * s, 0.16 * s,
                             facecolor="black", edgecolor="none"))
    # nose dot
    ax.add_patch(Polygon(
        np.array([[cx, cy + 0.03 * s],
                  [cx - 0.045*s, cy - 0.055 * s],
                  [cx + 0.045*s, cy - 0.055 * s]]),
        closed=True, facecolor="black", edgecolor="none"))


def draw():
    """Very dense hex-packed micro skulls – 14 columns, white on black.
    No crossbones, pure skull silhouette for maximum density readability.
    """
    fig, ax = setup_ax()

    cols  = 14
    hex_w = PERIOD / cols
    hex_h = hex_w * (np.sqrt(3) / 2)
    rows  = int(np.ceil(PERIOD / hex_h)) + 2
    s     = hex_w * 0.46

    for row in range(-1, rows + 1):
        offset = (hex_w * 0.5) if (row % 2 != 0) else 0.0
        for col in range(-1, cols + 2):
            cx = col * hex_w + offset + hex_w * 0.5
            cy = row * hex_h + hex_h * 0.5
            for ox, oy in WRAPS:
                skull_micro(ax, cx + ox, cy + oy, s)

    save(fig,
         "abstract halloween variation skull hex grid micro dense tiny packed "
         "pattern black white texture")


if __name__ == "__main__":
    draw()
