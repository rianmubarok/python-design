import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Circle
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


def bat_path(cx, cy, w, h):
    """Return a bat body + wings path polygon pts."""
    # Body
    t_body = np.linspace(0, 2 * np.pi, 30)
    bx = cx + w * 0.07 * np.cos(t_body)
    by = cy + h * 0.18 * np.sin(t_body)

    # Right wing
    rw = np.array([
        [cx + w * 0.07, cy],
        [cx + w * 0.30, cy + h * 0.22],
        [cx + w * 0.50, cy + h * 0.10],
        [cx + w * 0.38, cy - h * 0.20],
        [cx + w * 0.18, cy - h * 0.08],
        [cx + w * 0.07, cy],
    ])
    # Left wing (mirror)
    lw = rw.copy()
    lw[:, 0] = 2 * cx - lw[:, 0]

    # Head ears
    t_head = np.linspace(np.pi, 0, 20)
    hx = cx + w * 0.06 * np.cos(t_head)
    hy = cy + h * 0.18 + w * 0.10 * np.sin(t_head)

    all_pts = np.vstack([rw, lw[::-1]])
    return all_pts


def draw_bat(ax, cx, cy, w, h, fill="white"):
    pts = bat_path(cx, cy, w, h)
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 2) + [MPath.CLOSEPOLY]
    path = MPath(pts, codes)
    ax.add_patch(PathPatch(path, facecolor=fill, edgecolor="none", zorder=3))

    # Head circle
    ax.add_patch(Circle((cx, cy + h * 0.12), w * 0.07,
                        facecolor=fill, edgecolor="none", zorder=3))
    # Ears
    for ex in (-w * 0.04, w * 0.04):
        ear = np.array([
            [cx + ex, cy + h * 0.20],
            [cx + ex - w * 0.025, cy + h * 0.34],
            [cx + ex + w * 0.025, cy + h * 0.34],
        ])
        ax.add_patch(PathPatch(
            MPath(ear, [MPath.MOVETO, MPath.LINETO, MPath.CLOSEPOLY]),
            facecolor=fill, edgecolor="none", zorder=3))


def draw():
    """Staggered 4×4 grid of bats, each surrounded by 4 concentric ring halos.
    Rings decrease in opacity outward. White elements on black background."""
    fig, ax = setup_ax()

    cols, rows = 4, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    w = dx * 0.72
    h = dy * 0.55
    n_rings = 4

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    # Draw concentric aura rings (outermost first)
                    for k in range(n_rings, 0, -1):
                        r = w * 0.30 + k * w * 0.13
                        alpha = 0.18 + k * 0.10
                        ax.add_patch(Circle((px, py), r,
                                           facecolor="none",
                                           edgecolor="white",
                                           linewidth=1.2,
                                           alpha=min(alpha, 0.85),
                                           zorder=2))
                    draw_bat(ax, px, py, w, h, fill="white")

    save(fig, "abstract halloween variation bat concentric aura ring halo silhouette field pattern black white texture")


if __name__ == "__main__":
    draw()
