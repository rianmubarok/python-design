import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
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


def draw_eyeball(ax, cx, cy, rx, ry, fill_white="white", fill_iris="black", fill_pupil="white"):
    """Eyeball: white sclera ellipse, iris circle, pupil dot."""
    # Sclera
    ax.add_patch(Ellipse((cx, cy), rx * 2, ry * 2,
                         facecolor=fill_white, edgecolor="none", zorder=2))
    # Iris
    ir = min(rx, ry) * 0.55
    ax.add_patch(Circle((cx, cy), ir,
                        facecolor=fill_iris, edgecolor="none", zorder=3))
    # Pupil
    pr = ir * 0.45
    ax.add_patch(Circle((cx, cy), pr,
                        facecolor=fill_pupil, edgecolor="none", zorder=4))
    # Highlight dot
    ax.add_patch(Circle((cx + ir * 0.30, cy + ir * 0.30), pr * 0.35,
                        facecolor=fill_white, edgecolor="none", zorder=5))


def draw():
    """Dense brick-offset rows of eyeballs. White sclera on black background.
    Alternating rows shift by half-cell producing brick stagger.
    Iris is black, pupil white — creating concentric ring look."""
    fig, ax = setup_ax()

    cols, rows = 7, 8
    dx, dy = PERIOD / cols, PERIOD / rows
    rx = dx * 0.46
    ry = dy * 0.42

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -10 <= px <= PERIOD + 10 and -10 <= py <= PERIOD + 10:
                    draw_eyeball(ax, px, py, rx, ry)

    save(fig, "abstract halloween variation eyeball brick wall mosaic dense row stagger pattern black white texture")


if __name__ == "__main__":
    draw()
