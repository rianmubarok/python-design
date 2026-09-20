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


def bat_poly(cx, cy, s):
    """Wider, rounder wing variant — increased tip curve radius."""
    pts = np.array([
        [0.00,  0.10], [0.10,  0.22], [0.08,  0.06],
        [0.38,  0.28], [0.82,  0.46],
        [0.64,  0.10], [1.00,  0.16],
        [0.58, -0.06], [0.76, -0.32], [0.30, -0.10],
        [0.20, -0.26], [0.10, -0.08], [0.00, -0.20],
        [-0.10,-0.08],[-0.20,-0.26],[-0.30,-0.10],[-0.76,-0.32],
        [-0.58,-0.06],[-1.00, 0.16],[-0.64, 0.10],[-0.82, 0.46],
        [-0.38, 0.28],[-0.08, 0.06],[-0.10, 0.22],
    ])
    return pts * s + [cx, cy]


def draw():
    """4×5 large bat tessellation, staggered rows, black/white alternating fill."""
    fig, ax = setup_ax()
    cols, rows = 4, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.46
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            fill = "black" if (row + col) % 2 == 0 else "white"
            edge = "none" if fill == "black" else "black"
            inv  = "white" if fill == "black" else "black"
            for ox, oy in WRAPS:
                ax.add_patch(Polygon(bat_poly(cx+ox, cy+oy, s), closed=True,
                                     facecolor=fill, edgecolor=edge, linewidth=0.8))
                for ex in (-0.42*s, 0.42*s):
                    ax.add_patch(Circle((cx+ox+ex, cy+oy+0.28*s), 0.14*s,
                                        facecolor=inv, edgecolor="none"))
    save(fig, "abstract halloween variation bat tessellation large scale wide wingspan pattern black white texture")


if __name__ == "__main__":
    draw()
