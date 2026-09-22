import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch, Circle
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


def bat_poly(cx, cy, s, angle=0.0):
    pts = np.array([
        [0.00,  0.08], [0.12,  0.18], [0.10,  0.05], [0.42,  0.22], [0.78,  0.38],
        [0.62,  0.08], [0.95,  0.12], [0.55, -0.08], [0.72, -0.28], [0.28, -0.10],
        [0.18, -0.22], [0.08, -0.08], [0.00, -0.18],
        [-0.08,-0.08], [-0.18,-0.22], [-0.28,-0.10], [-0.72,-0.28],
        [-0.55,-0.08], [-0.95, 0.12], [-0.62, 0.08], [-0.78, 0.38],
        [-0.42, 0.22], [-0.10, 0.05], [-0.12, 0.18],
    ]) * s
    c, s_ = np.cos(angle), np.sin(angle)
    R = np.array([[c, -s_], [s_, c]])
    return (R @ pts.T).T + [cx, cy]


def coffin(ax, cx, cy, w, h, fill="black"):
    """Classic hexagonal coffin silhouette."""
    inv = "white" if fill == "black" else "black"
    # coffin body: trapezoid shoulders narrowing at head, then rectangular lower
    shoulder_w = w * 0.68
    body_w = w * 0.90
    top_y = cy + h * 0.50
    shoulder_y = cy + h * 0.22
    body_bot_y = cy - h * 0.50
    pts = np.array([
        [cx,               top_y],           # head top centre (narrow)
        [cx - shoulder_w * 0.5, shoulder_y], # left shoulder
        [cx - body_w * 0.5, cy],             # left widest
        [cx - body_w * 0.5, body_bot_y],     # bottom-left
        [cx + body_w * 0.5, body_bot_y],     # bottom-right
        [cx + body_w * 0.5, cy],
        [cx + shoulder_w * 0.5, shoulder_y],
        [cx,               top_y],
    ])
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor="none"))
    # cross detail
    cross_w = w * 0.09
    cross_h = h * 0.32
    cross_arm = w * 0.22
    arm_h = h * 0.06
    cross_cy = cy + h * 0.02
    ax.add_patch(FancyBboxPatch(
        (cx - cross_w * 0.5, cross_cy - cross_h * 0.5), cross_w, cross_h,
        boxstyle="round,pad=0,rounding_size=0.01",
        facecolor=inv, edgecolor="none"))
    ax.add_patch(FancyBboxPatch(
        (cx - cross_arm * 0.5, cross_cy + cross_h * 0.12), cross_arm, arm_h,
        boxstyle="round,pad=0,rounding_size=0.01",
        facecolor=inv, edgecolor="none"))


def draw():
    """6×6 checkerboard: even cells = bat silhouette, odd cells = coffin silhouette.
    Alternating black/white fill so they contrast with each other."""
    fig, ax = setup_ax()
    cols, rows = 6, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    bat_s = min(dx, dy) * 0.34
    cof_w = dx * 0.68
    cof_h = dy * 0.80

    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            is_bat = (row + col) % 2 == 0
            fill = "black" if (row + col) % 2 == 0 else "black"
            bg_fill = "black" if (row + col) % 2 == 0 else "white"
            # tile background square
            ax.add_patch(FancyBboxPatch(
                (cx - dx * 0.5, cy - dy * 0.5), dx, dy,
                boxstyle="square,pad=0",
                facecolor=bg_fill, edgecolor="none"))
            fg = "white" if bg_fill == "black" else "black"
            for ox, oy in WRAPS:
                if is_bat:
                    ax.add_patch(Polygon(
                        bat_poly(cx + ox, cy + oy, bat_s),
                        closed=True, facecolor=fg, edgecolor="none"))
                else:
                    coffin(ax, cx + ox, cy + oy, cof_w, cof_h, fill=fg)

    save(fig, "abstract halloween variation bat coffin checkerboard combo pattern black white texture")


if __name__ == "__main__":
    draw()
