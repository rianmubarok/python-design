import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse, Circle
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


def draw_ghost_body(ax, cx, cy, s, fill="white"):
    """Ghost silhouette path only (no eyes, for linking)."""
    inv = "black" if fill == "white" else "white"
    t_head = np.linspace(np.pi / 2, 0, 20)
    x_head = cx + (s * 0.28) * np.cos(t_head)
    y_head = cy + (s * 0.25) + (s * 0.28) * np.sin(t_head)
    x_body_r = np.array([cx + s * 0.28, cx + s * 0.34, cx + s * 0.36])
    y_body_r = np.array([cy + s * 0.25, cy, cy - s * 0.28])
    x_wave = np.linspace(cx + s * 0.36, cx - s * 0.36, 50)
    y_wave = (cy - s * 0.28) + (s * 0.07) * np.sin((x_wave - cx) / (s * 0.36) * 2.5 * np.pi)
    x_body_l = np.array([cx - s * 0.36, cx - s * 0.34, cx - s * 0.28])
    y_body_l = np.array([cy - s * 0.28, cy, cy + s * 0.25])
    t_head_l = np.linspace(np.pi, np.pi / 2, 20)
    x_head_l = cx + (s * 0.28) * np.cos(t_head_l)
    y_head_l = cy + (s * 0.25) + (s * 0.28) * np.sin(t_head_l)
    pts_x = np.concatenate([x_head, x_body_r, x_wave, x_body_l, x_head_l])
    pts_y = np.concatenate([y_head, y_body_r, y_wave, y_body_l, y_head_l])
    pts = np.column_stack([pts_x, pts_y])
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 2) + [MPath.CLOSEPOLY]
    path = MPath(pts, codes)
    edge = "black" if fill == "white" else "none"
    ax.add_patch(PathPatch(path, facecolor=fill, edgecolor=edge, linewidth=0.7, zorder=2))
    # Eyes
    for ex in (-s * 0.10, s * 0.10):
        ax.add_patch(Ellipse((cx + ex, cy + s * 0.25), s * 0.08, s * 0.12,
                             facecolor=inv, edgecolor="none", zorder=3))
    ax.add_patch(Ellipse((cx, cy + s * 0.10), s * 0.06, s * 0.09,
                         facecolor=inv, edgecolor="none", zorder=3))


def draw_link(ax, x1, y1, x2, y2, r, fill):
    """Draw a small rounded hand-link dot between two ghost centres."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ax.add_patch(Circle((mx, my), r, facecolor=fill, edgecolor="none", zorder=4))


def draw():
    """Horizontal rows of ghosts holding hands — linked by small circle dots.
    Even rows: white ghosts on black stripe. Odd rows: black ghosts on white stripe.
    Seamless via WRAPS."""
    fig, ax = setup_ax()

    rows = 6
    cols = 7
    dy = PERIOD / rows
    dx = PERIOD / cols
    s = dy * 0.50

    for row in range(rows):
        cy = (row + 0.5) * dy
        stripe_col = "black" if row % 2 == 0 else "white"
        ghost_fill = "white" if row % 2 == 0 else "black"

        # Draw stripe background for this row (for seamless y-wrap, draw via WRAPS)
        for ox, oy in WRAPS:
            from matplotlib.patches import Rectangle
            ax.add_patch(Rectangle(
                (0 + ox, row * dy + oy), PERIOD, dy,
                facecolor=stripe_col, edgecolor="none", zorder=0))

        shift = (dx * 0.5) if row % 2 else 0.0
        prev_x = None
        for col in range(-1, cols + 2):
            cx = col * dx + shift + dx * 0.5
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -5 <= py <= PERIOD + 5:
                    draw_ghost_body(ax, px, py, s, fill=ghost_fill)

            # Link dot between adjacent ghosts (same row, wrapped)
            if prev_x is not None:
                for ox, oy in WRAPS:
                    lx1, ly1 = prev_x + ox, cy + oy
                    lx2, ly2 = cx + ox, cy + oy
                    if -5 <= (lx1 + lx2) / 2 <= PERIOD + 5 and -5 <= ly1 <= PERIOD + 5:
                        draw_link(ax, lx1, ly1, lx2, ly2, s * 0.05,
                                  fill="black" if ghost_fill == "white" else "white")
            prev_x = cx

    save(fig, "abstract halloween variation ghost chain linked row stripe seamless pattern black white texture")


if __name__ == "__main__":
    draw()
