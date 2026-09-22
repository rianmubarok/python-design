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
    print(f"Saved: {jpg_path} | {svg_path}")


def corner_web(ax, cx, cy, max_r, angle_span, start_angle,
               n_spokes=7, n_rings=10, col="white"):
    """Quarter-web radiating from a corner point (cx, cy).
    angle_span in radians — covers a sector of the tile corner."""
    half = angle_span / 2
    angles = np.linspace(start_angle - half, start_angle + half, n_spokes)
    ring_radii = np.linspace(max_r * 0.08, max_r, n_rings)

    # spokes
    for a in angles:
        ax.plot([cx, cx + max_r * np.cos(a)],
                [cy, cy + max_r * np.sin(a)],
                color=col, linewidth=0.65, solid_capstyle="round")

    # concentric arcs (polygon segments)
    for r in ring_radii:
        arc_angles = np.linspace(start_angle - half, start_angle + half, 60)
        xs = cx + r * np.cos(arc_angles)
        ys = cy + r * np.sin(arc_angles)
        ax.plot(xs, ys, color=col, linewidth=0.50)

    # centre dot
    ax.add_patch(Circle((cx, cy), max_r * 0.022, facecolor=col, edgecolor="none"))


def draw():
    """Corner-burst spider web pattern — tile grid where every tile corner
    has a web quarter-circle exploding inward. Because corners are shared
    between 4 tiles, the four quarter-webs merge seamlessly at tile joins.
    Black background."""
    fig, ax = setup_ax()

    tile = 25.0          # tile size — 4×4 tiles in PERIOD=100
    cols = int(PERIOD / tile) + 1
    rows = int(PERIOD / tile) + 1
    max_r = tile * 0.72
    span = np.pi / 2     # 90° corner web

    # Corner angles: which direction a corner web radiates inward
    # Corner offsets and inward angles:
    # bottom-left corner → angle 45° (northeast)
    # bottom-right corner → angle 135° (northwest)
    # top-right corner → angle 225° (southwest)
    # top-left corner → angle 315° (southeast)
    corner_cfg = [
        (0.0,  0.0,  np.radians(45)),   # BL
        (1.0,  0.0,  np.radians(135)),  # BR
        (1.0,  1.0,  np.radians(225)),  # TR
        (0.0,  1.0,  np.radians(315)),  # TL
    ]

    for row in range(rows):
        for col in range(cols):
            for (fx, fy, ang) in corner_cfg:
                cx_base = col * tile + fx * tile
                cy_base = row * tile + fy * tile
                for ox, oy in WRAPS:
                    corner_web(ax, cx_base + ox, cy_base + oy,
                               max_r, span, ang,
                               n_spokes=8, n_rings=11)

    save(fig, "abstract halloween variation spider web corner burst quad tile pattern black white texture")


if __name__ == "__main__":
    draw()
