import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Circle
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


def draw_bat(ax, cx, cy, w, h, flip_y=False, fill="black"):
    """Bat silhouette. flip_y=True mirrors it upside-down."""
    sy = -1.0 if flip_y else 1.0
    edge = "none" if fill == "black" else "black"
    elw = 0.0 if fill == "black" else 0.8

    def pt(rx, ry):
        return (cx + rx * w, cy + sy * ry * h)

    # Wings as polygon
    wing = [
        pt(0.0,  0.00),
        pt(0.22, 0.28),
        pt(0.50, 0.14),
        pt(0.42, -0.22),
        pt(0.20, -0.08),
        pt(0.08, 0.00),
        pt(-0.08, 0.00),
        pt(-0.20, -0.08),
        pt(-0.42, -0.22),
        pt(-0.50, 0.14),
        pt(-0.22, 0.28),
        pt(0.0, 0.00),
    ]
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(wing) - 2) + [MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(wing, codes),
                           facecolor=fill, edgecolor=edge, linewidth=elw, zorder=2))

    # Head
    ax.add_patch(Circle(pt(0, 0.14), w * 0.07,
                        facecolor=fill, edgecolor=edge, linewidth=elw, zorder=3))

    # Ears
    for ex in (-0.045, 0.045):
        ear = [pt(ex, 0.22), pt(ex - 0.03, 0.38), pt(ex + 0.03, 0.38)]
        ax.add_patch(PathPatch(
            MPath(ear, [MPath.MOVETO, MPath.LINETO, MPath.CLOSEPOLY]),
            facecolor=fill, edgecolor=edge, linewidth=elw, zorder=3))


def draw():
    """Vertical columns of bats. Each column alternates up/down facing on every row.
    Within a column, odd rows are flipped. Adjacent columns are offset by half dy.
    Seamless tile."""
    fig, ax = setup_ax()

    cols, rows = 5, 7
    dx, dy = PERIOD / cols, PERIOD / rows
    w = dx * 0.44
    h = dy * 0.44

    for col in range(-1, cols + 1):
        cx = (col + 0.5) * dx
        for row in range(-1, rows + 1):
            # column offset: even cols start at 0, odd cols start at dy/2
            col_offset = (dy * 0.5) if col % 2 else 0.0
            cy = (row + 0.5) * dy + col_offset
            flip = bool(row % 2)
            fill = "black" if (col + row) % 2 == 0 else "black"  # all black on white
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    draw_bat(ax, px, py, w, h, flip_y=flip, fill="black")

    save(fig, "abstract halloween variation bat vertical column flip alternating up down direction pattern black white texture")


if __name__ == "__main__":
    draw()
