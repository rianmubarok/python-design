import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
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


def eyeball(ax, cx, cy, r, gaze_angle=0.0):
    """Eyeball with sclera, iris, pupil, iris rings, highlight."""
    # sclera
    ax.add_patch(Circle((cx, cy), r, facecolor="white", edgecolor="none", zorder=2))
    # iris
    iris_r = r * 0.54
    ax.add_patch(Circle((cx, cy), iris_r, facecolor="black", edgecolor="none", zorder=3))
    # iris detail rings
    for ring_r in np.linspace(iris_r * 0.62, iris_r * 0.94, 3):
        ax.add_patch(Circle((cx, cy), ring_r, facecolor="none",
                            edgecolor="white", linewidth=0.28, zorder=4))
    # pupil (offset for gaze)
    shift = iris_r * 0.20
    px = cx + shift * np.cos(gaze_angle)
    py = cy + shift * np.sin(gaze_angle)
    ax.add_patch(Circle((px, py), iris_r * 0.48,
                        facecolor="black", edgecolor="none", zorder=5))
    # highlight
    ax.add_patch(Circle((cx + r * 0.26, cy + r * 0.26), r * 0.11,
                        facecolor="white", edgecolor="none", zorder=6))


def draw():
    """Horizontal stripe bands of eyeballs. Each row gazes in the same direction
    but adjacent rows look in different directions (left, right, up, down…).
    Eyes within each row are uniformly sized and evenly spaced."""
    fig, ax = setup_ax()

    # gaze direction per row (cycles through 8 directions)
    gaze_dirs = [0, np.pi, np.pi/2, 3*np.pi/2,
                 np.pi/4, 5*np.pi/4, 3*np.pi/4, 7*np.pi/4]

    rows = 8
    cols = 10
    dy = PERIOD / rows
    dx = PERIOD / cols
    r = min(dx, dy) * 0.40

    for row in range(rows):
        gaze = gaze_dirs[row % len(gaze_dirs)]
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                eyeball(ax, cx + ox, cy + oy, r, gaze_angle=gaze)

    save(fig, "abstract halloween variation eyeball iris stripe band row gaze pattern black white texture")


if __name__ == "__main__":
    draw()
