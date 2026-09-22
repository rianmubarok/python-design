import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon, Circle
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


def draw_web_cracks(ax, cx, cy, r, n_spokes=7, n_rings=5, lw=0.9, color="white"):
    """Spider-web-style crack radiating from a point inside the skull."""
    ao = np.radians(12)
    spoke_angles = [ao + k * 2 * np.pi / n_spokes for k in range(n_spokes)]
    ring_radii = [r * (k + 1) / n_rings for k in range(n_rings)]

    for a in spoke_angles:
        ax.plot([cx, cx + r * np.cos(a)],
                [cy, cy + r * np.sin(a)],
                color=color, linewidth=lw, zorder=4)
    for ri in ring_radii:
        for k in range(n_spokes):
            a1 = spoke_angles[k]
            a2 = spoke_angles[(k + 1) % n_spokes]
            t = np.linspace(a1, a2, 16)
            ax.plot(cx + ri * np.cos(t), cy + ri * np.sin(t),
                    color=color, linewidth=lw * 0.8, zorder=4)


def skull(ax, cx, cy, s):
    """Large skull silhouette (black fill) with a spider-web crack overlaid on cranium."""
    fill = "black"
    inv = "white"
    skull_cy = cy + 0.08 * s

    # Cranium
    ax.add_patch(Ellipse((cx, skull_cy + 0.09 * s), 0.82 * s, 0.70 * s,
                         facecolor=fill, edgecolor="none", zorder=2))
    # Jaw
    ax.add_patch(FancyBboxPatch(
        (cx - 0.24 * s, skull_cy - 0.25 * s), 0.48 * s, 0.22 * s,
        boxstyle=f"round,pad=0,rounding_size={0.04*s:.4f}",
        facecolor=fill, edgecolor="none", zorder=2))

    # Eye sockets
    for ex in (-0.165 * s, 0.165 * s):
        ax.add_patch(Ellipse((cx + ex, skull_cy + 0.13 * s),
                             0.19 * s, 0.21 * s,
                             facecolor=inv, edgecolor="none", zorder=3))
    # Nose
    ax.add_patch(Polygon(
        [[cx, skull_cy + 0.01 * s],
         [cx - 0.06 * s, skull_cy - 0.09 * s],
         [cx + 0.06 * s, skull_cy - 0.09 * s]],
        closed=True, facecolor=inv, edgecolor="none", zorder=3))
    # Teeth — 3
    for tx in (-0.11 * s, 0.0, 0.11 * s):
        ax.add_patch(FancyBboxPatch(
            (cx + tx - 0.026 * s, skull_cy - 0.235 * s),
            0.052 * s, 0.10 * s,
            boxstyle="round,pad=0,rounding_size=0.004",
            facecolor=inv, edgecolor="none", zorder=3))

    # Spider-web cracks on cranium
    crack_cx = cx + s * 0.08
    crack_cy = skull_cy + s * 0.22
    draw_web_cracks(ax, crack_cx, crack_cy, s * 0.35,
                    n_spokes=7, n_rings=4, lw=1.2, color="white")


def draw():
    """2×2 macro skull tiles — each skull nearly fills its tile.
    Cranium covered in spider-web crack texture (white lines on black fill).
    Large, dramatic, close-up feel."""
    fig, ax = setup_ax()

    cols, rows = 2, 2
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.86

    for row in range(-1, rows + 1):
        for col in range(-1, cols + 1):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    skull(ax, px, py, s)

    save(fig, "abstract halloween variation skull macro oversized spiderweb crack cranium texture pattern black white texture")


if __name__ == "__main__":
    draw()
