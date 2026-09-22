import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse, FancyBboxPatch, Polygon, Circle
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


def draw_pumpkin_face(ax, cx, cy, s, fill="white"):
    """Pumpkin face — three lobes, stem, triangle eyes, jagged mouth."""
    inv = "black" if fill == "white" else "white"

    # Three lobes
    for ddx in (-s * 0.22, 0.0, s * 0.22):
        ax.add_patch(Ellipse((cx + ddx, cy), s * 0.30, s * 0.48,
                             facecolor=fill, edgecolor="none", zorder=2))
    # Stem
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.04, cy + s * 0.24), s * 0.08, s * 0.14,
        boxstyle=f"round,pad=0,rounding_size={s*0.015:.4f}",
        facecolor=fill, edgecolor="none", zorder=2))
    # Triangle eyes
    for ex in (-s * 0.13, s * 0.13):
        eye = np.array([
            [cx + ex,          cy + s * 0.12],
            [cx + ex - s*0.07, cy - s * 0.01],
            [cx + ex + s*0.07, cy - s * 0.01],
        ])
        ax.add_patch(Polygon(eye, closed=True, facecolor=inv, edgecolor="none", zorder=3))
    # Jagged mouth
    x_m = np.array([-0.17, -0.11, -0.05, 0.0, 0.05, 0.11, 0.17]) * s + cx
    y_m = np.array([-0.14, -0.07, -0.14, -0.07, -0.14, -0.07, -0.14]) * s + cy
    x_cl = np.array([0.17, 0.17, -0.17, -0.17]) * s + cx
    y_cl = np.array([-0.07, -0.18, -0.18, -0.14]) * s + cy
    mx = np.concatenate([x_m, x_cl])
    my = np.concatenate([y_m, y_cl])
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(mx) - 2) + [MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(np.column_stack([mx, my]), codes),
                           facecolor=inv, edgecolor="none", zorder=3))


def draw_petal_web(ax, cx, cy, tile_w, tile_h, n_rings=6, lw=0.9):
    """Radial web following the same seamless pattern as the ghost-web reference:
    - half_diag radius so spokes reach all four corners
    - 8 spokes at 45° increments (aligns symmetrically on a square tile)
    - rings drawn arc-by-arc between adjacent spokes (not full circles)
    - no alpha, solid lines — same style as ghost-web"""
    half_diag = 0.5 * np.hypot(tile_w, tile_h)
    max_r = half_diag

    n_spokes = 8
    spoke_angles = [k * 2 * np.pi / n_spokes for k in range(n_spokes)]
    ring_radii = [max_r * (k + 1) / n_rings for k in range(n_rings)]

    # Spokes
    for a in spoke_angles:
        ax.plot([cx, cx + max_r * np.cos(a)],
                [cy, cy + max_r * np.sin(a)],
                color="white", linewidth=lw, zorder=1)

    # Rings — arc segment by segment between spokes (matches ghost-web pattern)
    for r in ring_radii:
        for k in range(n_spokes):
            a1 = spoke_angles[k]
            a2 = spoke_angles[(k + 1) % n_spokes]
            t = np.linspace(a1, a2, 20)
            ax.plot(cx + r * np.cos(t), cy + r * np.sin(t),
                    color="white", linewidth=lw * 0.80, zorder=1)


def draw():
    """2×2 macro tiles. Each tile: large pumpkin face centred, surrounded by a full
    radial petal web. Same seamless technique as the ghost-web reference:
    half-diagonal spokes + arc-segment rings + wide guard."""
    fig, ax = setup_ax()

    cols, rows = 2, 2
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.72

    for row in range(-1, rows + 1):
        for col in range(-1, cols + 1):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -30 <= px <= PERIOD + 30 and -30 <= py <= PERIOD + 30:
                    draw_petal_web(ax, px, py, dx, dy, n_rings=6)
                    draw_pumpkin_face(ax, px, py, s, fill="white")

    save(fig, "abstract halloween variation jack o lantern radial petal web negative space macro tile pattern black white texture")


if __name__ == "__main__":
    draw()
