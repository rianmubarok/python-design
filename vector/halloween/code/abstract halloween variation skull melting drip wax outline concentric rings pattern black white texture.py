import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon, PathPatch, Circle
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


def skull_outline_with_drip(ax, cx, cy, s):
    """Skull outline (white stroke only) that melts downward with drip tendrils."""
    fill = "none"
    stroke = "white"
    lw = s * 0.04

    skull_cy = cy + 0.08 * s

    # Cranium outline
    t = np.linspace(0, 2 * np.pi, 80)
    ex, ey = 0.82 * s * 0.5, 0.68 * s * 0.5
    ax.plot(cx + ex * np.cos(t), skull_cy + 0.09*s + ey * np.sin(t),
            color=stroke, linewidth=lw, zorder=2)

    # Jaw outline
    jaw_pts_x = np.array([cx - 0.24*s, cx - 0.24*s, cx + 0.24*s, cx + 0.24*s])
    jaw_pts_y = np.array([skull_cy - 0.07*s, skull_cy - 0.26*s,
                          skull_cy - 0.26*s, skull_cy - 0.07*s])
    ax.plot(jaw_pts_x, jaw_pts_y, color=stroke, linewidth=lw * 0.8, zorder=2)

    # Eye socket outlines
    for epx in (-0.165 * s, 0.165 * s):
        t2 = np.linspace(0, 2 * np.pi, 40)
        ax.plot(cx + epx + 0.095*s * np.cos(t2),
                skull_cy + 0.13*s + 0.105*s * np.sin(t2),
                color=stroke, linewidth=lw * 0.75, zorder=3)

    # Concentric ring auras (outline only — creates halo rings around skull)
    for k in range(1, 5):
        r = s * (0.44 + k * 0.10)
        ax.plot(cx + r * np.cos(t), cy + r * np.sin(t),
                color=stroke, linewidth=lw * 0.55, alpha=0.50 - k * 0.07, zorder=1)

    # Drip tendrils downward
    rng = np.random.default_rng(abs(hash((round(cx, 1), round(cy, 1)))) % (2**32))
    n_drips = 5
    drip_xs = np.linspace(cx - s*0.18, cx + s*0.18, n_drips)
    for dx2 in drip_xs:
        drip_len = rng.uniform(s*0.12, s*0.30)
        # Smooth drip path
        t_d = np.linspace(0, 1, 20)
        jitter = rng.uniform(-s*0.015, s*0.015, 20)
        xd = dx2 + jitter
        yd = (skull_cy - s*0.26) - drip_len * t_d
        # Bulge at tip
        bulge = np.where(t_d > 0.85, (t_d - 0.85) * 6 * s * 0.025, 0)
        xd[1::2] += bulge[1::2] * 0.5
        ax.plot(xd, yd, color=stroke, linewidth=lw * 0.9, zorder=2)
        # Drip blob
        ax.add_patch(Circle((xd[-1], yd[-1]), s * 0.022,
                            facecolor=stroke, edgecolor="none", zorder=3))


def draw():
    """3×3 grid of skull-drip-ring combos.
    Each skull is rendered as a white outline only (no solid fill),
    surrounded by concentric ring halos and melting drip lines downward.
    Eerie, ghostly aesthetic on black background."""
    fig, ax = setup_ax()

    cols, rows = 3, 3
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.76

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    skull_outline_with_drip(ax, px, py, s)

    save(fig, "abstract halloween variation skull melting drip wax outline concentric rings pattern black white texture")


if __name__ == "__main__":
    draw()
