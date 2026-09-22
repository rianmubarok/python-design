import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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


def coffin_pts(cx, cy, w, h):
    """Return normalised coffin polygon points centred at (cx, cy).
    Coffin shape: wide shoulders tapering to narrow foot and head.
         shoulder_w = w (full width at shoulder)
         head_w     = w * 0.55 (narrower at top)
         foot_w     = w * 0.45 (narrowest at bottom tip)
    Y axis: top = +h/2, bottom = -h/2."""
    hw  = w  * 0.50
    shw = w  * 0.50   # shoulder half-width (widest)
    hew = w  * 0.275  # head half-width
    fow = w  * 0.225  # foot half-width
    hh  = h  * 0.50

    # Clockwise from top-left shoulder
    pts = [
        (cx - hew, cy + hh),            # head top-left
        (cx + hew, cy + hh),            # head top-right
        (cx + shw, cy + hh * 0.45),     # shoulder right
        (cx + shw, cy - hh * 0.15),     # waist right
        (cx + fow, cy - hh),            # foot bottom-right
        (cx - fow, cy - hh),            # foot bottom-left
        (cx - shw, cy - hh * 0.15),     # waist left
        (cx - shw, cy + hh * 0.45),     # shoulder left
    ]
    return pts


def draw_coffin(ax, cx, cy, w, h, fill="white"):
    """Draw a coffin polygon."""
    edge = "black" if fill == "white" else "none"
    elw  = 0.5      if fill == "white" else 0.0
    ax.add_patch(Polygon(coffin_pts(cx, cy, w, h), closed=True,
                         facecolor=fill, edgecolor=edge,
                         linewidth=elw, zorder=2))


def draw():
    """Coffins interlocked tip-to-base in vertical chains across the canvas.
    Each chain alternates fill (black coffin then white coffin).
    Adjacent chains are offset vertically by half a coffin height,
    and coffin heads of one chain nestle between the feet of the next chain
    — creating a tight interlocking tessellation. Seamless."""
    fig, ax = setup_ax()

    cols = 6
    cw   = PERIOD / cols          # coffin width
    ch   = cw * 1.80              # coffin height (tall)
    # Vertical step: coffins stack head-to-foot with a tiny overlap
    vstep = ch * 0.95             # slight overlap so tips interlock

    rows_needed = int(np.ceil(PERIOD / vstep)) + 3

    for col in range(-1, cols + 1):
        cx = (col + 0.5) * cw
        # Alternate chain offset
        row_offset = vstep * 0.5 if col % 2 else 0.0

        for row in range(-2, rows_needed):
            cy = row * vstep + row_offset - vstep * 0.5
            fill = "white" if (row + col) % 2 == 0 else "black"

            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -ch <= px <= PERIOD + ch and -ch <= py <= PERIOD + ch:
                    draw_coffin(ax, px, py, cw * 0.92, ch * 0.92, fill=fill)

    save(fig, "abstract halloween variation coffin interlocking tip to base chain seamless pattern black white texture")


if __name__ == "__main__":
    draw()
