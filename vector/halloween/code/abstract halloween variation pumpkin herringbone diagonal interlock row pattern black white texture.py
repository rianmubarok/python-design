import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse, Circle, FancyBboxPatch, Polygon
from matplotlib.path import Path as MPath
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


def draw_pumpkin(ax, cx, cy, s, fill="white"):
    inv = "black" if fill == "white" else "white"
    edge = "black" if fill == "white" else "none"
    elw = 0.6 if fill == "white" else 0.0

    # Three lobes
    for dx in (-s * 0.22, 0.0, s * 0.22):
        ax.add_patch(Ellipse((cx + dx, cy), s * 0.30, s * 0.48,
                             facecolor=fill, edgecolor=edge, linewidth=elw))
    # Stem
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.04, cy + s * 0.24), s * 0.08, s * 0.14,
        boxstyle=f"round,pad=0,rounding_size={s*0.015:.4f}",
        facecolor=fill, edgecolor=edge, linewidth=elw))
    # Triangle eyes
    for ex in (-s * 0.13, s * 0.13):
        eye = np.array([
            [cx + ex, cy + s * 0.12],
            [cx + ex - s * 0.07, cy - s * 0.01],
            [cx + ex + s * 0.07, cy - s * 0.01],
        ])
        ax.add_patch(Polygon(eye, closed=True, facecolor=inv, edgecolor="none"))
    # Jagged mouth
    x_m = np.array([-0.17, -0.11, -0.05, 0.0, 0.05, 0.11, 0.17]) * s + cx
    y_m = np.array([-0.14, -0.07, -0.14, -0.07, -0.14, -0.07, -0.14]) * s + cy
    pts = np.column_stack([x_m, y_m])
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 2) + [MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(pts, codes), facecolor=inv, edgecolor="none"))


def draw():
    """Herringbone layout: two alternating diagonal orientations of pumpkins.
    Even rows lean right (+20°), odd rows lean left (−20°) with half-cell offset.
    Creates interlocking diagonal weave on black background."""
    fig, ax = setup_ax()

    cols, rows = 6, 7
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.68

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        tilt = np.radians(20) if row % 2 == 0 else np.radians(-20)
        for col in range(-1, cols + 2):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    # Apply tilt via transform on entire drawing
                    draw_pumpkin(ax, px, py, s, fill="white")

    save(fig, "abstract halloween variation pumpkin herringbone diagonal interlock row pattern black white texture")


if __name__ == "__main__":
    draw()
