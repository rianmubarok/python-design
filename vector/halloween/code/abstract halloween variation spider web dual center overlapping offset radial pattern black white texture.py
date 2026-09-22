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


def draw_web(ax, cx, cy, max_r, n_spokes=8, n_rings=6, angle_offset=0.0, lw=0.8):
    """Single radial spider web centred at cx,cy."""
    spokes_a = [angle_offset + k * 2 * np.pi / n_spokes for k in range(n_spokes)]
    ring_radii = [max_r * (k + 1) / n_rings for k in range(n_rings)]

    # Draw spokes
    for a in spokes_a:
        ax.plot([cx, cx + max_r * np.cos(a)],
                [cy, cy + max_r * np.sin(a)],
                color="white", linewidth=lw, zorder=2)

    # Draw concentric ring segments
    for r in ring_radii:
        for k in range(n_spokes):
            a1 = spokes_a[k]
            a2 = spokes_a[(k + 1) % n_spokes]
            t = np.linspace(a1, a2, 20)
            ax.plot(cx + r * np.cos(t), cy + r * np.sin(t),
                    color="white", linewidth=lw, zorder=2)


def draw():
    """2×2 tile. Each tile has TWO overlapping webs:
    one centred at (dx*0.35, dy*0.35) and another at (dx*0.65, dy*0.65),
    their radii large enough to overlap and interfere visually.
    On black background — pure white thread lines."""
    fig, ax = setup_ax()

    cols, rows = 2, 2
    dx, dy = PERIOD / cols, PERIOD / rows
    r = min(dx, dy) * 0.45

    offsets = [(-0.18, -0.18), (0.18, 0.18)]
    angle_offsets = [0.0, np.radians(22.5)]

    for row in range(-1, rows + 1):
        for col in range(-1, cols + 1):
            tile_cx = (col + 0.5) * dx
            tile_cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = tile_cx + ox, tile_cy + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    for (ofdx, ofdy), ao in zip(offsets, angle_offsets):
                        draw_web(ax, px + ofdx * dx, py + ofdy * dy,
                                 r, n_spokes=8, n_rings=6, angle_offset=ao, lw=0.9)

    save(fig, "abstract halloween variation spider web dual center overlapping offset radial pattern black white texture")


if __name__ == "__main__":
    draw()
