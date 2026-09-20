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
    print(f"Saved: {jpg_path}")


def moon_phase(ax, cx, cy, r, phase):
    """Draw a moon at the given phase (0=new, 0.5=full, 1=new again).
    Phase 0-0.25: waxing crescent→quarter
    Phase 0.25-0.5: quarter→gibbous→full
    Phase 0.5-0.75: waning gibbous→quarter
    Phase 0.75-1.0: waning crescent→new"""
    # Always draw the lit disc
    ax.add_patch(Circle((cx, cy), r, facecolor="white", edgecolor="none", zorder=2))

    if phase < 0.02 or phase > 0.98:
        # New moon — all dark
        ax.add_patch(Circle((cx, cy), r, facecolor="black", edgecolor="none", zorder=3))
        return

    # Shadow offset along x-axis: negative=left shadow (waxing), positive=right(waning)
    # phase 0→0.5: waxing  (shadow retreats from right to left)
    # phase 0.5→1: waning  (shadow advances from left to right)
    if phase <= 0.5:
        # waxing: p=0 fully dark, p=0.5 fully lit
        shadow_frac = 1.0 - 2 * phase       # 1→0
        shadow_xoff = r * shadow_frac * 1.1
        ax.add_patch(Circle((cx + shadow_xoff, cy), r, facecolor="black",
                            edgecolor="none", zorder=3))
    else:
        # waning: p=0.5 fully lit, p=1 fully dark
        shadow_frac = 2 * (phase - 0.5)     # 0→1
        shadow_xoff = -r * shadow_frac * 1.1
        ax.add_patch(Circle((cx + shadow_xoff, cy), r, facecolor="black",
                            edgecolor="none", zorder=3))


def draw():
    """Moon phase sequence strip — 8 phases repeated across columns, multiple rows.
    Each row is offset by 4 phases so neighbour rows show complementary moons."""
    fig, ax = setup_ax()
    phases_per_row = 8
    rows = 8
    dx = PERIOD / phases_per_row
    dy = PERIOD / rows
    r = min(dx, dy) * 0.42

    for row in range(rows):
        offset = (row % 2) * 4   # shift every other row by half cycle
        for col in range(phases_per_row):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            phase = ((col + offset) % phases_per_row) / phases_per_row
            for ox, oy in WRAPS:
                moon_phase(ax, cx + ox, cy + oy, r, phase)
    save(fig, "abstract halloween variation moon phase sequence strip repeating pattern black white texture")


if __name__ == "__main__":
    draw()
