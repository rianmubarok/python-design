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


def star6(cx, cy, r):
    """6-pointed star: two overlapping equilateral triangles."""
    pts = []
    for i in range(6):
        ang = -np.pi/2 + i * np.pi/3
        rad = r if i % 2 == 0 else r * 0.577  # inner = 1/sqrt(3)*outer
        pts.append([cx + rad*np.cos(ang), cy + rad*np.sin(ang)])
    return np.array(pts)


def draw():
    """Alternating crescent moons and 6-pointed stars on checker grid, scaled up."""
    fig, ax = setup_ax()
    n = 7
    step = PERIOD / n
    for row in range(n):
        for col in range(n):
            cx = (col + 0.5)*step
            cy = (row + 0.5)*step
            for ox, oy in WRAPS:
                x, y = cx+ox, cy+oy
                if (row+col) % 2 == 0:
                    # crescent — larger
                    ax.add_patch(Circle((x, y), 4.5, facecolor="black", edgecolor="none"))
                    ax.add_patch(Circle((x+1.35, y+0.4), 3.6, facecolor="white", edgecolor="none"))
                else:
                    # 6-pointed star — larger
                    ax.add_patch(Polygon(star6(x, y, 3.6), closed=True,
                                         facecolor="black", edgecolor="none"))
                    # inner cutout star (smaller)
                    ax.add_patch(Polygon(star6(x, y, 1.4), closed=True,
                                         facecolor="white", edgecolor="none"))
    save(fig, "abstract halloween variation moon star of david six point lattice scaled pattern black white texture")


if __name__ == "__main__":
    draw()
