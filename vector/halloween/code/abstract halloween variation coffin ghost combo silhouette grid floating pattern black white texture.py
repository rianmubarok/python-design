import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse, FancyBboxPatch, Polygon
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


def draw_coffin(ax, cx, cy, w, h, fill="white"):
    """Coffin silhouette: hexagonal body, wider at shoulders, tapering at foot."""
    sw = w * 0.70   # shoulder width
    fw = w * 0.55   # foot width
    hw = w * 0.50   # head width
    sh = h * 0.30   # shoulder offset from top
    pts = [
        (cx,         cy + h * 0.50),     # top centre
        (cx + hw/2,  cy + h * 0.50),
        (cx + sw/2,  cy + h * 0.50 - sh),
        (cx + fw/2,  cy - h * 0.50),
        (cx - fw/2,  cy - h * 0.50),
        (cx - sw/2,  cy + h * 0.50 - sh),
        (cx - hw/2,  cy + h * 0.50),
    ]
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor="none", zorder=1))


def draw_ghost(ax, cx, cy, s, fill="black"):
    """Small ghost floating above coffin."""
    inv = "white" if fill == "black" else "black"

    t_r = np.linspace(np.pi / 2, 0, 20)
    x_r = cx + s * 0.26 * np.cos(t_r)
    y_r = cy + s * 0.22 + s * 0.26 * np.sin(t_r)

    x_br = np.array([cx + s * 0.26, cx + s * 0.34, cx + s * 0.35])
    y_br = np.array([cy + s * 0.22, cy, cy - s * 0.24])

    x_wave = np.linspace(cx + s * 0.35, cx - s * 0.35, 40)
    y_wave = (cy - s * 0.24) + s * 0.055 * np.sin((x_wave - cx) / (s * 0.35) * 2.5 * np.pi)

    x_bl = np.array([cx - s * 0.35, cx - s * 0.34, cx - s * 0.26])
    y_bl = np.array([cy - s * 0.24, cy, cy + s * 0.22])

    t_l = np.linspace(np.pi, np.pi / 2, 20)
    x_l = cx + s * 0.26 * np.cos(t_l)
    y_l = cy + s * 0.22 + s * 0.26 * np.sin(t_l)

    pts_x = np.concatenate([x_r, x_br, x_wave, x_bl, x_l])
    pts_y = np.concatenate([y_r, y_br, y_wave, y_bl, y_l])
    pts = np.column_stack([pts_x, pts_y])
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 2) + [MPath.CLOSEPOLY]
    ec = "none"
    ax.add_patch(PathPatch(MPath(pts, codes),
                           facecolor=fill, edgecolor=ec, linewidth=0, zorder=3))

    for ex in (-s * 0.09, s * 0.09):
        ax.add_patch(Ellipse((cx + ex, cy + s * 0.21), s * 0.07, s * 0.10,
                             facecolor=inv, edgecolor="none", zorder=4))
    ax.add_patch(Ellipse((cx, cy + s * 0.08), s * 0.06, s * 0.08,
                         facecolor=inv, edgecolor="none", zorder=4))


def draw():
    """3×4 grid. Each cell: white coffin on black bg, with a tiny black ghost
    floating out of the open top of the coffin. Ghost appears to be rising from it."""
    fig, ax = setup_ax()

    cols, rows = 4, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    cw = dx * 0.62
    ch = dy * 0.78
    gs = min(dx, dy) * 0.28

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    draw_coffin(ax, px, py, cw, ch, fill="white")
                    # Ghost hovers just above the coffin top
                    draw_ghost(ax, px, py + ch * 0.46 + gs * 0.32, gs, fill="black")

    save(fig, "abstract halloween variation coffin ghost combo silhouette grid floating pattern black white texture")


if __name__ == "__main__":
    draw()
