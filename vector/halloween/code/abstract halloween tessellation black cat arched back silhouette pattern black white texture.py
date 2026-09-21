import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon
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


def arched_cat(ax, cx, cy, s, fill="black", inv="white", flip=False):
    """Black cat in classic Halloween arched-back pose — side profile silhouette."""
    sx = -1 if flip else 1   # horizontal mirror

    # body — arched ellipse (tilted)
    body_w = s * 0.58
    body_h = s * 0.35
    body_cx = cx
    body_cy = cy + s * 0.06
    ax.add_patch(Ellipse((body_cx, body_cy), body_w, body_h,
                         angle=10 * sx, facecolor=fill, edgecolor="none"))

    # arched back hump
    back_pts = []
    n = 40
    for i in range(n + 1):
        t = np.pi * i / n   # 0 to pi
        bx = body_cx + sx * (body_w / 2 - body_w * i / n)
        by = body_cy + body_h / 2 + s * 0.18 * np.sin(t)
        back_pts.append([bx, by])
    back_pts.append([body_cx - sx * body_w / 2, body_cy])
    back_pts.append([body_cx + sx * body_w / 2, body_cy])
    ax.add_patch(Polygon(back_pts, closed=True, facecolor=fill, edgecolor="none"))

    # head
    head_r = s * 0.20
    head_cx = cx + sx * body_w * 0.38
    head_cy = body_cy + body_h * 0.28 + head_r * 0.3
    ax.add_patch(Circle((head_cx, head_cy), head_r, facecolor=fill, edgecolor="none"))

    # ears (triangular)
    for ear_side, ear_x_off in [(1, head_r * 0.45), (-1, -head_r * 0.45)]:
        ear_pts = np.array([
            [head_cx + ear_x_off * sx, head_cy + head_r * 0.65],
            [head_cx + (ear_x_off - head_r * 0.28) * sx, head_cy + head_r * 1.40],
            [head_cx + (ear_x_off + head_r * 0.18) * sx, head_cy + head_r * 1.45],
        ])
        ax.add_patch(Polygon(ear_pts, closed=True, facecolor=fill, edgecolor="none"))

    # eye — slitted
    ax.add_patch(Ellipse((head_cx + sx * head_r * 0.18, head_cy + head_r * 0.12),
                         head_r * 0.32, head_r * 0.22,
                         facecolor=inv, edgecolor="none"))
    ax.add_patch(Ellipse((head_cx + sx * head_r * 0.18, head_cy + head_r * 0.12),
                         head_r * 0.08, head_r * 0.22,
                         facecolor=fill, edgecolor="none"))

    # legs — 4 short stubs
    for i, lx_off in enumerate([-0.30, -0.10, 0.12, 0.30]):
        leg_cx = body_cx + sx * body_w * lx_off
        ax.add_patch(Ellipse((leg_cx, body_cy - body_h * 0.46),
                             s * 0.085, s * 0.20,
                             facecolor=fill, edgecolor="none"))

    # tail — curling up behind body
    t = np.linspace(0, np.pi * 1.5, 80)
    tail_start_x = body_cx - sx * body_w * 0.44
    tail_start_y = body_cy
    tail_xs = tail_start_x + sx * (-s * 0.28 * np.sin(t) - t * s * 0.04)
    tail_ys = tail_start_y + s * 0.22 * (1 - np.cos(t)) - t * s * 0.01
    # draw tail as thick line
    for j in range(len(t) - 1):
        ax.plot([tail_xs[j], tail_xs[j + 1]], [tail_ys[j], tail_ys[j + 1]],
                color=fill, linewidth=2.8, solid_capstyle="round")


def draw():
    """Seamless arched black cat tessellation — alternating mirror/flip orientation."""
    fig, ax = setup_ax()
    cols, rows = 5, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.80
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            flip = (row + col) % 2 == 1
            fill = "black" if (row + col) % 2 == 0 else "white"
            inv = "white" if fill == "black" else "black"
            bg = inv
            ax.add_patch(Polygon([
                [cx - dx / 2, cy - dy / 2],
                [cx + dx / 2, cy - dy / 2],
                [cx + dx / 2, cy + dy / 2],
                [cx - dx / 2, cy + dy / 2],
            ], closed=True, facecolor=bg, edgecolor="none"))
            for ox, oy in WRAPS:
                arched_cat(ax, cx + ox, cy + oy, s, fill=fill, inv=inv, flip=flip)
    save(fig, "abstract halloween tessellation black cat arched back silhouette pattern black white texture")


if __name__ == "__main__":
    draw()
