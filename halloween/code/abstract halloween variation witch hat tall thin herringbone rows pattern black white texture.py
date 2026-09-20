import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
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
EPS_DIR = OUTPUT_DIR / \"eps\"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


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
    eps_path = EPS_DIR / f\"{name} {DATE}.eps\"
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format=\"eps\", pad_inches=0, facecolor=\"white\", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path} | {eps_path}")


def tall_hat(ax, cx, cy, fill, w_scale=1.0, h_scale=1.0):
    """Tall thin witch hat — cone height exaggerated, brim narrow."""
    inv = "white" if fill == "black" else "black"
    edge = "none" if fill == "black" else "black"

    bw = 4.2 * w_scale   # brim half-width
    ch = 9.5 * h_scale   # cone height (very tall)
    cw = 2.4 * w_scale   # cone base half-width

    cone = np.array([
        [cx,       cy + ch],
        [cx - cw,  cy - 0.5],
        [cx + cw,  cy - 0.5]
    ])
    brim = np.array([
        [cx - bw, cy - 0.5],
        [cx + bw, cy - 0.5],
        [cx + bw * 0.85, cy - 1.8],
        [cx - bw * 0.85, cy - 1.8]
    ])
    band = np.array([
        [cx - cw * 0.90, cy + 0.2],
        [cx + cw * 0.90, cy + 0.2],
        [cx + cw * 0.78, cy - 0.55],
        [cx - cw * 0.78, cy - 0.55]
    ])

    ax.add_patch(Polygon(cone, closed=True, facecolor=fill, edgecolor=edge, linewidth=0.7))
    ax.add_patch(Polygon(brim, closed=True, facecolor=fill, edgecolor=edge, linewidth=0.7))
    ax.add_patch(Polygon(band, closed=True, facecolor=inv, edgecolor="none"))
    # buckle
    ax.add_patch(FancyBboxPatch(
        (cx - 0.55, cy - 0.42), 1.1, 0.88,
        boxstyle="round,pad=0,rounding_size=0.12",
        facecolor=inv, edgecolor="none"))


def draw():
    """Tall thin hats in a herringbone arrangement — alternating lean left/right,
    tightly packed in rows with half-row offset."""
    fig, ax = setup_ax()
    cols, rows = 9, 7
    dx, dy = PERIOD / cols, PERIOD / rows

    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            # herringbone: alternate lean
            lean = (row + col) % 2
            fill = "black" if (row + col) % 2 == 0 else "white"
            # slightly thinner on odd positions
            ws = 0.85 if lean else 1.0
            for ox, oy in WRAPS:
                tall_hat(ax, cx + ox, cy + oy, fill, w_scale=ws)
    save(fig, "abstract halloween variation witch hat tall thin herringbone rows pattern black white texture")


if __name__ == "__main__":
    draw()
