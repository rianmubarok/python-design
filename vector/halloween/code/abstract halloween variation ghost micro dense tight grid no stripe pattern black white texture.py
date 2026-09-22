import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse
from matplotlib.path import Path as MPath
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI  = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR  = SCRIPT_DIR.parent / "output"
JPG_DIR     = OUTPUT_DIR / "jpg"
SVG_DIR     = OUTPUT_DIR / "svg"
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


def draw_ghost(ax, cx, cy, s):
    """Minimal white ghost on black — compact silhouette, tiny wavy hem."""
    t_head = np.linspace(np.pi / 2, 0, 16)
    x_head = cx + (s * 0.26) * np.cos(t_head)
    y_head = cy + (s * 0.22) + (s * 0.26) * np.sin(t_head)

    x_body_r = np.array([cx + s * 0.26, cx + s * 0.32, cx + s * 0.34])
    y_body_r = np.array([cy + s * 0.22, cy, cy - s * 0.26])

    x_wave = np.linspace(cx + s * 0.34, cx - s * 0.34, 40)
    y_wave = (cy - s * 0.26) + (s * 0.05) * np.sin((x_wave - cx) / (s * 0.34) * 3.0 * np.pi)

    x_body_l = np.array([cx - s * 0.34, cx - s * 0.32, cx - s * 0.26])
    y_body_l = np.array([cy - s * 0.26, cy, cy + s * 0.22])

    t_head_l = np.linspace(np.pi, np.pi / 2, 16)
    x_head_l = cx + (s * 0.26) * np.cos(t_head_l)
    y_head_l = cy + (s * 0.22) + (s * 0.26) * np.sin(t_head_l)

    pts_x = np.concatenate([x_head, x_body_r, x_wave, x_body_l, x_head_l])
    pts_y = np.concatenate([y_head, y_body_r, y_wave, y_body_l, y_head_l])
    pts   = np.column_stack([pts_x, pts_y])
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 2) + [MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(pts, codes), facecolor="white",
                           edgecolor="none", zorder=2))

    # tiny eyes
    for ex in (-s * 0.09, s * 0.09):
        ax.add_patch(Ellipse((cx + ex, cy + s * 0.24), s * 0.065, s * 0.090,
                             facecolor="black", edgecolor="none", zorder=3))
    ax.add_patch(Ellipse((cx, cy + s * 0.10), s * 0.055, s * 0.075,
                         facecolor="black", edgecolor="none", zorder=3))


def draw():
    """Dense micro grid of tiny ghosts — 10 cols × 12 rows, pure white on black.
    No background stripes, no alternating fill — uniform white ghosts.
    Odd rows offset by half cell for hex-like stagger.
    """
    fig, ax = setup_ax()
    cols, rows = 10, 12
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.72

    for row in range(rows):
        shift = dx * 0.5 if row % 2 else 0.0
        for col in range(cols):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -10 <= px <= PERIOD + 10 and -10 <= py <= PERIOD + 10:
                    draw_ghost(ax, px, py, s)

    save(fig,
         "abstract halloween variation ghost micro dense tight grid no stripe "
         "pattern black white texture")


if __name__ == "__main__":
    draw()
