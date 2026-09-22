import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Circle
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


def witch_hat(ax, cx, cy, s, fill="black"):
    inv = "white" if fill == "black" else "black"
    edge = "none" if fill == "black" else "black"
    # cone
    cone = np.array([[cx, cy + s * 0.50],
                     [cx - s * 0.22, cy - s * 0.14],
                     [cx + s * 0.22, cy - s * 0.14]])
    ax.add_patch(Polygon(cone, closed=True, facecolor=fill,
                         edgecolor=edge, linewidth=0.6))
    # brim
    brim = np.array([[cx - s * 0.52, cy - s * 0.14],
                     [cx + s * 0.52, cy - s * 0.14],
                     [cx + s * 0.46, cy - s * 0.26],
                     [cx - s * 0.46, cy - s * 0.26]])
    ax.add_patch(Polygon(brim, closed=True, facecolor=fill,
                         edgecolor=edge, linewidth=0.6))
    # band
    band = np.array([[cx - s * 0.20, cy - s * 0.03],
                     [cx + s * 0.20, cy - s * 0.03],
                     [cx + s * 0.18, cy - s * 0.10],
                     [cx - s * 0.18, cy - s * 0.10]])
    ax.add_patch(Polygon(band, closed=True, facecolor=inv, edgecolor="none"))


def crescent_moon(ax, cx, cy, r, fill="black", tilt_deg=0):
    """Crescent drawn via two circles. Slightly tilted."""
    inv = "white" if fill == "black" else "black"
    # outer disc
    ax.add_patch(Circle((cx, cy), r, facecolor=fill, edgecolor="none"))
    # offset inner disc punches out crescent
    tilt = np.radians(tilt_deg)
    offset = r * 0.40
    ax.add_patch(Circle((cx + offset * np.cos(tilt),
                          cy + offset * np.sin(tilt)),
                         r * 0.78, facecolor=inv, edgecolor="none"))


def draw():
    """Alternating rows: odd rows = witch hats, even rows = crescent moons.
    Odd hat rows are shifted half a step right; both alternate black/white fill."""
    fig, ax = setup_ax()
    cols = 6
    rows = 8
    dx, dy = PERIOD / cols, PERIOD / rows
    hat_s = min(dx, dy) * 0.78
    moon_r = min(dx, dy) * 0.34

    for row in range(rows):
        for col in range(cols):
            shift = dx * 0.5 if row % 2 else 0.0
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            fill = "black" if (row + col) % 2 == 0 else "white"
            is_hat = row % 2 == 0

            for ox, oy in WRAPS:
                if is_hat:
                    witch_hat(ax, cx + ox, cy + oy, hat_s, fill=fill)
                else:
                    crescent_moon(ax, cx + ox, cy + oy, moon_r,
                                  fill=fill, tilt_deg=30)

    save(fig, "abstract halloween variation witch hat crescent moon alternating row interlocked pattern black white texture")


if __name__ == "__main__":
    draw()
