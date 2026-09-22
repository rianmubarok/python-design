import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Wedge
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


def draw_web_sector(ax, cx, cy, max_r, n_rings, n_spokes, start_angle_deg,
                    sector_count, fill_alt=True):
    """Spider web built from concentric ring arcs and radial spoke lines,
    then sliced into `sector_count` pie-wedge sectors with alternating fill.

    The filled sectors are white; gaps (unfilled) reveal the black background.
    Ring lines and spoke lines are drawn in white on top."""
    sector_angle = 360.0 / sector_count
    radii = [max_r * (k + 1) / n_rings for k in range(n_rings)]

    # Filled alternating wedge sectors (every other sector)
    for s in range(sector_count):
        if (s % 2 == 0) == fill_alt:
            a0 = start_angle_deg + s * sector_angle
            a1 = a0 + sector_angle
            ax.add_patch(Wedge((cx, cy), max_r, a0, a1,
                               facecolor="white", edgecolor="none",
                               linewidth=0, zorder=1))

    # Black concentric ring gaps (cut rings into alternating fill)
    for k, r in enumerate(radii):
        ring_fill = "black" if k % 2 == 0 else "none"
        if ring_fill == "black":
            # Draw black annular ring to carve alternating rings
            inner_r = radii[k - 1] if k > 0 else 0
            ax.add_patch(Wedge((cx, cy), r, start_angle_deg,
                               start_angle_deg + 360,
                               width=r - inner_r,
                               facecolor="black", edgecolor="none", zorder=2))

    # White concentric arc lines
    lw = 0.6
    for r in radii:
        theta = np.linspace(0, 2 * np.pi, 360)
        ax.plot(cx + r * np.cos(theta), cy + r * np.sin(theta),
                color="white", lw=lw, zorder=3)

    # White radial spoke lines
    spoke_angles = np.linspace(0, 2 * np.pi, n_spokes, endpoint=False)
    spoke_angles += np.radians(start_angle_deg)
    for ang in spoke_angles:
        ax.plot([cx, cx + max_r * np.cos(ang)],
                [cy, cy + max_r * np.sin(ang)],
                color="white", lw=lw, zorder=3)

    # Central hub dot
    ax.add_patch(Circle((cx, cy), max_r * 0.045,
                        facecolor="white", edgecolor="none", zorder=4))


def draw():
    """3×3 grid of spider web tiles, each a concentric-ring web sliced into
    alternating filled/empty pie sectors. Rotation offsets vary per tile.
    Seamless via WRAPS."""
    fig, ax = setup_ax()

    cols, rows = 3, 3
    dx, dy = PERIOD / cols, PERIOD / rows
    max_r = min(dx, dy) * 0.47

    # Vary sector count and start angle per tile for visual interest
    configs = [
        (6, 0),  (8, 22),  (6, 15),
        (8, 10), (6, 30),  (8, 5),
        (6, 20), (8, 45),  (6, 35),
    ]
    idx = 0
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            n_sec, start_a = configs[idx % len(configs)]
            fill_alt = (idx % 2 == 0)
            idx += 1
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    draw_web_sector(ax, px, py, max_r,
                                    n_rings=5, n_spokes=n_sec,
                                    start_angle_deg=start_a,
                                    sector_count=n_sec,
                                    fill_alt=fill_alt)

    save(fig, "abstract halloween variation spider web concentric rings sector slice cut pattern black white texture")


if __name__ == "__main__":
    draw()
