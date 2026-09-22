import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Polygon
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
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


def draw_tombstone(ax, cx, cy, w, h, fill="black"):
    """Classic tombstone: rectangular base + semicircular arch top.
    Engraved 'RIP' represented by 3 small horizontal notch lines.
    """
    inv = "white" if fill == "black" else "black"
    # Body rectangle (lower 60%)
    body_h = h * 0.60
    body_y = cy - h * 0.50
    ax.add_patch(FancyBboxPatch(
        (cx - w * 0.40, body_y), w * 0.80, body_h,
        boxstyle="square,pad=0",
        facecolor=fill, edgecolor="none"))

    # Arch cap (upper 40%): half-ellipse
    arch_cy = body_y + body_h
    arch_rx = w * 0.40
    arch_ry = h * 0.40
    theta = np.linspace(0, np.pi, 60)
    arch_x = cx + arch_rx * np.cos(theta)
    arch_y = arch_cy + arch_ry * np.sin(theta)
    left_x  = cx - arch_rx
    right_x = cx + arch_rx
    pts = (list(zip(arch_x, arch_y)) +
           [(right_x, arch_cy), (left_x, arch_cy)])
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor="none"))

    # "RIP" — 3 short engraved lines in the centre
    rip_cx = cx
    rip_cy = body_y + body_h * 0.55
    for i, dy_off in enumerate([-0.06 * h, 0.0, 0.06 * h]):
        lw = w * (0.28 if i == 0 else 0.22 if i == 1 else 0.18)
        ax.add_patch(FancyBboxPatch(
            (rip_cx - lw * 0.5, rip_cy + dy_off - h * 0.012),
            lw, h * 0.024,
            boxstyle="square,pad=0",
            facecolor=inv, edgecolor="none"))


def draw():
    """Tombstones arranged in staggered rows — silhouette horizon bands.
    5 cols × 4 rows. Black tombstones on white background.
    Row heights give a panoramic graveyard skyline repeating tile.
    """
    fig, ax = setup_ax()
    cols, rows = 5, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    w = dx * 0.72
    h = dy * 0.80

    for row in range(rows):
        shift = dx * 0.5 if row % 2 else 0.0
        for col in range(cols):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                draw_tombstone(ax, cx + ox, cy + oy, w, h, fill="black")

    save(fig,
         "abstract halloween variation tombstone silhouette horizon row stripe "
         "repeating pattern black white texture")


if __name__ == "__main__":
    draw()
