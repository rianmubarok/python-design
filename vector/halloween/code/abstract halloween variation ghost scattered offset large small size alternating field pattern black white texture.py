import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse
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


def draw_ghost(ax, cx, cy, s, fill="white"):
    """Simple smooth ghost silhouette."""
    inv = "black" if fill == "white" else "white"
    t_head = np.linspace(np.pi / 2, 0, 20)
    x_head = cx + (s * 0.28) * np.cos(t_head)
    y_head = cy + (s * 0.25) + (s * 0.28) * np.sin(t_head)
    x_body_r = np.array([cx + s * 0.28, cx + s * 0.35, cx + s * 0.38])
    y_body_r = np.array([cy + s * 0.25, cy, cy - s * 0.30])
    x_wave = np.linspace(cx + s * 0.38, cx - s * 0.38, 50)
    y_wave = (cy - s * 0.30) + (s * 0.06) * np.sin((x_wave - cx) / (s * 0.38) * 2.5 * np.pi)
    x_body_l = np.array([cx - s * 0.38, cx - s * 0.35, cx - s * 0.28])
    y_body_l = np.array([cy - s * 0.30, cy, cy + s * 0.25])
    t_head_l = np.linspace(np.pi, np.pi / 2, 20)
    x_head_l = cx + (s * 0.28) * np.cos(t_head_l)
    y_head_l = cy + (s * 0.25) + (s * 0.28) * np.sin(t_head_l)
    pts_x = np.concatenate([x_head, x_body_r, x_wave, x_body_l, x_head_l])
    pts_y = np.concatenate([y_head, y_body_r, y_wave, y_body_l, y_head_l])
    pts = np.column_stack([pts_x, pts_y])
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 2) + [MPath.CLOSEPOLY]
    path = MPath(pts, codes)
    edge = "black" if fill == "white" else "none"
    ax.add_patch(PathPatch(path, facecolor=fill, edgecolor=edge, linewidth=0.8, zorder=2))
    for ex in (-s * 0.10, s * 0.10):
        ax.add_patch(Ellipse((cx + ex, cy + s * 0.25), s * 0.08, s * 0.12,
                             facecolor=inv, edgecolor="none", zorder=3))
    ax.add_patch(Ellipse((cx, cy + s * 0.10), s * 0.07, s * 0.10,
                         facecolor=inv, edgecolor="none", zorder=3))


def draw():
    """Scattered ghost field: large ghosts on a regular staggered grid,
    small ghost tucked into every gap — alternating large/small by cell parity."""
    fig, ax = setup_ax()

    # Large ghost grid — 5 cols × 5 rows staggered
    cols_l, rows_l = 5, 5
    dx_l, dy_l = PERIOD / cols_l, PERIOD / rows_l
    s_large = min(dx_l, dy_l) * 0.55

    # Small ghost grid — 10 cols × 10 rows (fills gaps)
    cols_s, rows_s = 10, 10
    dx_s, dy_s = PERIOD / cols_s, PERIOD / rows_s
    s_small = min(dx_s, dy_s) * 0.28

    rng = np.random.default_rng(42)

    # Draw small ghosts first (background layer)
    for row in range(rows_s):
        shift_s = (dx_s * 0.5) if row % 2 else 0.0
        for col in range(cols_s):
            # skip cells that will be occupied by large ghosts (even parity)
            if (row // 2 + col // 2) % 2 == 0 and row % 2 == 0 and col % 2 == 0:
                continue
            cx = (col + 0.5) * dx_s + shift_s + rng.uniform(-dx_s * 0.12, dx_s * 0.12)
            cy = (row + 0.5) * dy_s + rng.uniform(-dy_s * 0.12, dy_s * 0.12)
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -10 <= px <= PERIOD + 10 and -10 <= py <= PERIOD + 10:
                    draw_ghost(ax, px, py, s_small, fill="white")

    # Draw large ghosts on top
    for row in range(rows_l):
        shift_l = (dx_l * 0.5) if row % 2 else 0.0
        for col in range(cols_l):
            cx = (col + 0.5) * dx_l + shift_l
            cy = (row + 0.5) * dy_l
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    draw_ghost(ax, px, py, s_large, fill="white")

    save(fig, "abstract halloween variation ghost scattered offset large small size alternating field pattern black white texture")


if __name__ == "__main__":
    draw()
