import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse, Polygon
from matplotlib.path import Path as MPath
from pathlib import Path
from datetime import datetime

matplotlib.use("Agg")

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


def draw_ghost(ax, cx, cy, s, fill="black", inv="white"):
    """Chubby, round ghost — wider body, softer wavy hem, large round head."""
    # Outer body contour — wider and rounder than original
    t_head = np.linspace(np.pi / 2, 0, 24)
    x_head = cx + (s * 0.36) * np.cos(t_head)
    y_head = cy + (s * 0.22) + (s * 0.36) * np.sin(t_head)

    x_body_r = np.array([cx + s * 0.36, cx + s * 0.44, cx + s * 0.46])
    y_body_r = np.array([cy + s * 0.22, cy, cy - s * 0.28])

    # Fewer, shallower waves → chubbier hem
    x_wave = np.linspace(cx + s * 0.46, cx - s * 0.46, 60)
    y_wave = (cy - s * 0.28) + (s * 0.07) * np.sin((x_wave - cx) / (s * 0.46) * 2.0 * np.pi)

    x_body_l = np.array([cx - s * 0.46, cx - s * 0.44, cx - s * 0.36])
    y_body_l = np.array([cy - s * 0.28, cy, cy + s * 0.22])

    t_head_l = np.linspace(np.pi, np.pi / 2, 24)
    x_head_l = cx + (s * 0.36) * np.cos(t_head_l)
    y_head_l = cy + (s * 0.22) + (s * 0.36) * np.sin(t_head_l)

    pts_x = np.concatenate([x_head, x_body_r, x_wave, x_body_l, x_head_l])
    pts_y = np.concatenate([y_head, y_body_r, y_wave, y_body_l, y_head_l])
    pts   = np.column_stack([pts_x, pts_y])

    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 2) + [MPath.CLOSEPOLY]
    edge  = "black" if fill == "white" else "none"
    ax.add_patch(PathPatch(MPath(pts, codes), facecolor=fill,
                           edgecolor=edge, linewidth=1.5, zorder=2))

    # Large, wide-set eyes
    for ex in (-s * 0.14, s * 0.14):
        ax.add_patch(Ellipse((cx + ex, cy + s * 0.30), s * 0.11, s * 0.15,
                             facecolor=inv, edgecolor="none", zorder=3))
    # Round mouth
    ax.add_patch(Ellipse((cx, cy + s * 0.12), s * 0.09, s * 0.12,
                         facecolor=inv, edgecolor="none", zorder=3))


def draw():
    """Large-scale zigzag ghost grid — 4 cols × 5 rows, big chubby ghosts.
    Odd rows shift right by half-cell; alternating black/white per row.
    Black rows get black background stripe for contrast.
    """
    fig, ax = setup_ax()
    cols, rows = 4, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.85   # big, almost fills the cell

    for row in range(rows):
        fill = "black" if row % 2 == 0 else "white"
        inv  = "white" if fill == "black" else "black"
        bg   = "black" if fill == "black" else "white"
        if bg == "black":
            ax.add_patch(Polygon(
                [[0, row * dy], [PERIOD, row * dy],
                 [PERIOD, (row + 1) * dy], [0, (row + 1) * dy]],
                closed=True, facecolor="black", edgecolor="none", zorder=1))

        shift = dx * 0.5 if row % 2 else 0.0
        for col in range(cols):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                    draw_ghost(ax, px, py, s, fill=fill, inv=inv)

    save(fig,
         "abstract halloween variation ghost zigzag fat round large scale "
         "pattern black white texture")


if __name__ == "__main__":
    draw()
