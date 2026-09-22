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


def draw_black_cat(ax, cx, cy, s, fill="black"):
    """Stylised arched-back black cat silhouette."""
    inv = "white" if fill == "black" else "black"
    # Body — arched ellipse
    ax.add_patch(Ellipse((cx, cy), s * 0.58, s * 0.36,
                         angle=15, facecolor=fill, edgecolor="none"))
    # Head
    ax.add_patch(Circle((cx + s * 0.22, cy + s * 0.18), s * 0.18,
                        facecolor=fill, edgecolor="none"))
    # Ears (two triangles)
    for ex, ea in [(-s * 0.09, -0.06), (s * 0.08, 0.06)]:
        ear = np.array([
            [cx + s * 0.22 + ex,         cy + s * 0.30],
            [cx + s * 0.22 + ex - s*0.07, cy + s * 0.18],
            [cx + s * 0.22 + ex + s*0.07, cy + s * 0.18],
        ])
        ax.add_patch(Polygon(ear, closed=True, facecolor=fill, edgecolor="none"))
    # Tail — curved strip on the left
    t = np.linspace(0, np.pi * 0.9, 30)
    tx = cx - s * 0.28 + s * 0.12 * np.cos(t)
    ty = cy - s * 0.10 + s * 0.22 * np.sin(t)
    ax.plot(tx, ty, color=fill, linewidth=s * 0.14, solid_capstyle="round")
    # Eyes
    for ex in (-s * 0.045, s * 0.045):
        ax.add_patch(Ellipse((cx + s * 0.22 + ex, cy + s * 0.20),
                             s * 0.055, s * 0.068,
                             facecolor=inv, edgecolor="none"))


def draw_witch_hat(ax, cx, cy, s, fill="black"):
    """Compact witch hat (cone + brim)."""
    # Cone
    cone = np.array([
        [cx,            cy + s * 0.42],
        [cx - s * 0.14, cy - s * 0.04],
        [cx + s * 0.14, cy - s * 0.04],
    ])
    ax.add_patch(Polygon(cone, closed=True, facecolor=fill, edgecolor="none"))
    # Brim ellipse
    ax.add_patch(Ellipse((cx, cy - s * 0.02), s * 0.38, s * 0.10,
                         facecolor=fill, edgecolor="none"))
    # Band
    ax.add_patch(Ellipse((cx, cy + s * 0.02), s * 0.17, s * 0.045,
                         facecolor="white" if fill == "black" else "black",
                         edgecolor="none"))


def draw():
    """Alternating columns: odd columns = black cats (stacked), even columns = witch hats.
    Each column is a single repeated motif, creating a strong vertical stripe rhythm.
    White background, all elements black. Seamless tile."""
    fig, ax = setup_ax()

    cols = 6
    rows_cat = 5
    rows_hat = 6
    dx = PERIOD / cols

    for col in range(-1, cols + 1):
        cx_centre = (col + 0.5) * dx
        if col % 2 == 0:
            # Cat column
            dy = PERIOD / rows_cat
            for row in range(-1, rows_cat + 1):
                cy = (row + 0.5) * dy
                s = dx * 0.76
                for ox, oy in WRAPS:
                    px, py = cx_centre + ox, cy + oy
                    if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                        draw_black_cat(ax, px, py, s, fill="black")
        else:
            # Hat column
            dy = PERIOD / rows_hat
            for row in range(-1, rows_hat + 1):
                cy = (row + 0.5) * dy
                s = dx * 0.72
                for ox, oy in WRAPS:
                    px, py = cx_centre + ox, cy + oy
                    if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                        draw_witch_hat(ax, px, py, s, fill="black")

    save(fig, "abstract halloween variation black cat witch hat vertical column stripe pair pattern black white texture")


if __name__ == "__main__":
    draw()
