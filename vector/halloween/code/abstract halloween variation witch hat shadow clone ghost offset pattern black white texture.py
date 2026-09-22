import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch
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


def hat_silhouette(ax, cx, cy, s, fill="black", alpha=1.0):
    """Full witch hat silhouette: cone + brim + band."""
    inv = "white" if fill == "black" else "black"
    cone = np.array([[cx, cy + s * 0.52],
                     [cx - s * 0.24, cy - s * 0.16],
                     [cx + s * 0.24, cy - s * 0.16]])
    brim = np.array([[cx - s * 0.54, cy - s * 0.16],
                     [cx + s * 0.54, cy - s * 0.16],
                     [cx + s * 0.48, cy - s * 0.29],
                     [cx - s * 0.48, cy - s * 0.29]])
    band = np.array([[cx - s * 0.22, cy - s * 0.04],
                     [cx + s * 0.22, cy - s * 0.04],
                     [cx + s * 0.20, cy - s * 0.12],
                     [cx - s * 0.20, cy - s * 0.12]])
    ax.add_patch(Polygon(cone,  closed=True, facecolor=fill, edgecolor="none", alpha=alpha))
    ax.add_patch(Polygon(brim,  closed=True, facecolor=fill, edgecolor="none", alpha=alpha))
    ax.add_patch(Polygon(band,  closed=True, facecolor=inv,  edgecolor="none", alpha=alpha))


def draw():
    """Shadow-clone witch hat — each hat is preceded by 2 ghost copies shifted
    diagonally down-right at decreasing alpha, creating a trailing shadow illusion.
    5×5 grid, staggered rows, black hats on white."""
    fig, ax = setup_ax()
    cols, rows = 5, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.76

    shadow_steps = 3
    shadow_dx = s * 0.14   # each shadow offset step
    shadow_dy = -s * 0.10

    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                # draw shadows first (back to front)
                for step in range(shadow_steps, 0, -1):
                    sdx = shadow_dx * step
                    sdy = shadow_dy * step
                    alpha = 0.12 + 0.08 * (shadow_steps - step)
                    hat_silhouette(ax, cx + ox + sdx, cy + oy + sdy,
                                   s, fill="black", alpha=alpha)
                # primary hat on top
                hat_silhouette(ax, cx + ox, cy + oy, s, fill="black", alpha=1.0)

    save(fig, "abstract halloween variation witch hat shadow clone ghost offset pattern black white texture")


if __name__ == "__main__":
    draw()
