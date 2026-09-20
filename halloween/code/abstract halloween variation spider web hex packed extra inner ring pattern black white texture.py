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


def web(ax, cx, cy, r, twist=0.0):
    spokes = 8
    angles = [k * np.pi / 4 + twist for k in range(spokes)]
    for a in angles:
        ax.plot([cx, cx + r*np.cos(a)], [cy, cy + r*np.sin(a)],
                color="black", linewidth=0.75)
    # extra inner ring at 0.14 scale + standard rings
    for sc in (0.14, 0.28, 0.50, 0.72, 0.96):
        pts = np.array([[cx + r*sc*np.cos(a), cy + r*sc*np.sin(a)] for a in angles])
        pts = np.vstack([pts, pts[0]])
        lw = 0.8 if sc == 0.14 else 0.55
        ax.plot(pts[:, 0], pts[:, 1], color="black", linewidth=lw)
    ax.add_patch(Circle((cx, cy), 0.28, facecolor="black", edgecolor="none"))


def draw():
    """Hex-packed offset spider webs, 9×9, tighter inner ring added."""
    fig, ax = setup_ax()
    cols, rows = 9, 9
    dx, dy = PERIOD / cols, PERIOD / rows
    r = min(dx, dy) * 0.60
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5)*dx + (dx*0.5 if row % 2 else 0)
            cy = (row + 0.5)*dy
            twist = np.pi/8 if (row+col) % 2 else 0.0
            for ox, oy in WRAPS:
                web(ax, cx+ox, cy+oy, r, twist)
    save(fig, "abstract halloween variation spider web hex packed extra inner ring pattern black white texture")


if __name__ == "__main__":
    draw()
