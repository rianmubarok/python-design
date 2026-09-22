import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
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


def moon_phase_patch(ax, cx, cy, r, phase, fill="white", bg="black"):
    """Draw one moon phase.
    phase: 0=new(dark), 1=waxing crescent, 2=first quarter, 3=waxing gibbous,
           4=full, 5=waning gibbous, 6=last quarter, 7=waning crescent.
    Uses a terminator offset to simulate illumination fraction."""
    # Full circle in bg colour first
    ax.add_patch(Circle((cx, cy), r, facecolor=bg, edgecolor="none", zorder=1))

    if phase == 0:
        return  # new moon — all dark

    if phase == 4:
        # Full moon
        ax.add_patch(Circle((cx, cy), r, facecolor=fill, edgecolor="none", zorder=2))
        return

    n = 200
    # Right half of circle (illuminated side for waxing; flipped for waning)
    flip = phase > 4
    theta = np.linspace(-np.pi / 2, np.pi / 2, n)
    right_x = cx + r * np.cos(theta)
    right_y = cy + r * np.sin(theta)

    # Terminator: ellipse with semi-major = r, semi-minor varies with phase
    # phase 1→ crescent: terminator bulges far left
    # phase 3→ gibbous: terminator barely dips inward
    frac = (phase % 4) / 4.0          # 0.25, 0.5, 0.75 → crescent, quarter, gibbous
    term_a = r * np.abs(np.cos(frac * np.pi))   # semi-minor of terminator ellipse
    sign = 1 if phase in (1, 2, 3) else -1      # waxing: terminator left; waning: right
    term_x = cx + sign * term_a * np.cos(theta + np.pi)  # terminator curve
    term_y = cy + r * np.sin(theta)

    # For quarter phase the terminator is a straight vertical line
    if phase in (2, 6):
        term_x = np.full(n, cx)

    if not flip:
        # Waxing: illuminate right side, terminator on left boundary
        pts_x = np.concatenate([right_x, term_x[::-1]])
        pts_y = np.concatenate([right_y, term_y[::-1]])
    else:
        # Waning: illuminate left side
        left_theta = np.linspace(np.pi / 2, 3 * np.pi / 2, n)
        left_x = cx + r * np.cos(left_theta)
        left_y = cy + r * np.sin(left_theta)
        pts_x = np.concatenate([left_x, term_x])
        pts_y = np.concatenate([left_y, term_y])

    pts = np.column_stack([pts_x, pts_y])
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor="none", zorder=2))


def draw_quartet(ax, tile_cx, tile_cy, cell_r, phases, fill, bg):
    """Draw a 2×2 sub-grid of 4 moon phases within one tile."""
    offsets = [(-cell_r * 0.55, cell_r * 0.55),   # top-left
               ( cell_r * 0.55, cell_r * 0.55),   # top-right
               (-cell_r * 0.55, -cell_r * 0.55),  # bottom-left
               ( cell_r * 0.55, -cell_r * 0.55)]  # bottom-right
    for (ox, oy), phase in zip(offsets, phases):
        moon_phase_patch(ax, tile_cx + ox, tile_cy + oy,
                         cell_r * 0.48, phase, fill=fill, bg=bg)


def draw():
    """4×4 tile grid; each tile is a 2×2 quartet of moon phases.
    Tiles alternate between white-on-black and inverted themes.
    Phase sequence rotates across tiles for visual rhythm."""
    fig, ax = setup_ax()

    tile_cols, tile_rows = 4, 4
    tdx = PERIOD / tile_cols
    tdy = PERIOD / tile_rows
    cell_r = min(tdx, tdy) * 0.28   # radius of each moon within sub-cell

    # Phase groups: each tile gets 4 consecutive phases from the 8-phase cycle
    phase_cycle = [1, 2, 3, 4, 5, 6, 7, 4]   # repeating quartet sequences

    tile_idx = 0
    for row in range(tile_rows):
        for col in range(tile_cols):
            tcx = (col + 0.5) * tdx
            tcy = (row + 0.5) * tdy
            fill = "white" if (row + col) % 2 == 0 else "black"
            bg   = "black" if fill == "white" else "white"

            # 4 phases for this tile
            start = (tile_idx * 2) % len(phase_cycle)
            phases = [phase_cycle[(start + k) % len(phase_cycle)] for k in range(4)]
            tile_idx += 1

            for ox, oy in WRAPS:
                px, py = tcx + ox, tcy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    draw_quartet(ax, px, py, cell_r, phases, fill=fill, bg=bg)

    save(fig, "abstract halloween variation crescent moon phase waxing waning quartet tile pattern black white texture")


if __name__ == "__main__":
    draw()
