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
    print(f"Saved: {jpg_path}")


def coffin_pts(cx, cy, w, h):
    """Classic 6-sided coffin silhouette centred at (cx, cy).
    Narrow at the foot, wider at the shoulder, then tapers slightly to the head."""
    hw = w / 2
    # relative proportions (y from -0.5 to 0.5)
    # foot: narrow, shoulder: wide, head: medium-wide
    pts = np.array([
        [cx - hw * 0.40,  cy - h * 0.50],   # foot-left
        [cx + hw * 0.40,  cy - h * 0.50],   # foot-right
        [cx + hw * 1.00,  cy - h * 0.18],   # lower-right shoulder
        [cx + hw * 0.78,  cy + h * 0.50],   # head-right
        [cx - hw * 0.78,  cy + h * 0.50],   # head-left
        [cx - hw * 1.00,  cy - h * 0.18],   # lower-left shoulder
    ])
    return pts


def draw():
    """Seamless coffin tessellation — coffins packed in a staggered brick grid,
    alternating black and white fill."""
    fig, ax = setup_ax()
    cols, rows = 6, 7
    dx, dy = PERIOD / cols, PERIOD / rows
    cw = dx * 0.88
    ch = dy * 0.90
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            fill = "black" if (row + col) % 2 == 0 else "white"
            edge = "none" if fill == "black" else "black"
            for ox, oy in WRAPS:
                pts = coffin_pts(cx + ox, cy + oy, cw, ch)
                ax.add_patch(Polygon(pts, closed=True, facecolor=fill,
                                     edgecolor=edge, linewidth=0.7))
                # cross detail on the lid
                cx2, cy2 = cx + ox, cy + oy
                inv = "white" if fill == "black" else "black"
                ax.plot([cx2, cx2], [cy2 + ch * 0.05, cy2 + ch * 0.35],
                        color=inv, linewidth=1.2)
                ax.plot([cx2 - cw * 0.18, cx2 + cw * 0.18], [cy2 + ch * 0.22, cy2 + ch * 0.22],
                        color=inv, linewidth=1.2)
    save(fig, "abstract halloween tessellation coffin silhouette interlocking grid pattern black white texture")


if __name__ == "__main__":
    draw()
