import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
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


def draw_candy_corn(ax, cx, cy, length, angle, fill_base="white", fill_mid="#888888"):
    """Single candy corn pointing in direction `angle` from base at (cx,cy)."""
    offset = length * 0.08
    sx = cx + offset * np.cos(angle)
    sy = cy + offset * np.sin(angle)
    eff = length - offset
    perp = angle + np.pi / 2

    def band(ax_, p0x, p0y, hw0, p1x, p1y, hw1, fc):
        s0 = [(p0x + hw0 * np.cos(perp), p0y + hw0 * np.sin(perp)),
              (p0x - hw0 * np.cos(perp), p0y - hw0 * np.sin(perp))]
        s1 = [(p1x - hw1 * np.cos(perp), p1y - hw1 * np.sin(perp)),
              (p1x + hw1 * np.cos(perp), p1y + hw1 * np.sin(perp))]
        ax_.add_patch(Polygon(s0 + s1, closed=True, facecolor=fc, edgecolor="none"))

    # Three bands: base (widest), mid, tip (point)
    b0x, b0y = sx, sy
    b1x = sx + eff * 0.36 * np.cos(angle); b1y = sy + eff * 0.36 * np.sin(angle)
    b2x = sx + eff * 0.70 * np.cos(angle); b2y = sy + eff * 0.70 * np.sin(angle)
    tipx = sx + eff * np.cos(angle);        tipy = sy + eff * np.sin(angle)

    w0 = eff * 0.18
    w1 = eff * 0.11
    w2 = eff * 0.06

    band(ax, b0x, b0y, w0, b1x, b1y, w0, fill_base)
    band(ax, b1x, b1y, w0, b2x, b2y, w1, fill_mid)
    # tip triangle
    pts_tip = [
        (b2x + w1 * np.cos(perp), b2y + w1 * np.sin(perp)),
        (b2x - w1 * np.cos(perp), b2y - w1 * np.sin(perp)),
        (tipx, tipy)
    ]
    ax.add_patch(Polygon(pts_tip, closed=True, facecolor=fill_base, edgecolor="none"))


def draw():
    """Horizontal rows of candy corns in a zigzag: within each row,
    alternate pieces point UP then DOWN (tip alternates direction).
    Even rows  → white candy corns on black stripe.
    Odd rows   → grey candy corns on white stripe (inverted).
    Brick-offset between rows for seamless tiling."""
    fig, ax = setup_ax()

    rows = 7
    cols = 8
    dy = PERIOD / rows
    dx = PERIOD / cols
    length = dy * 0.82

    for row in range(rows):
        bg   = "black" if row % 2 == 0 else "white"
        base = "white" if bg == "black"  else "black"
        mid  = "#888888" if bg == "black" else "#777777"

        for ox, oy in WRAPS:
            ax.add_patch(Rectangle(
                (0 + ox, row * dy + oy), PERIOD, dy,
                facecolor=bg, edgecolor="none", zorder=0))

        shift = (dx * 0.5) if row % 2 else 0.0
        cy = (row + 0.5) * dy

        for col in range(-1, cols + 2):
            cx = col * dx + shift + dx * 0.5
            # Zigzag: even col → point up (angle=π/2), odd col → point down (angle=-π/2)
            angle = np.pi / 2 if col % 2 == 0 else -np.pi / 2

            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -10 <= px <= PERIOD + 10 and -5 <= py <= PERIOD + 5:
                    draw_candy_corn(ax, px, py, length, angle,
                                   fill_base=base, fill_mid=mid)

    save(fig, "abstract halloween variation candy corn zigzag alternating point direction row stripe pattern black white texture")


if __name__ == "__main__":
    draw()
