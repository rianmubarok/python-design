import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyBboxPatch, Polygon
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
    print(f"Saved: {jpg_path}")


def gothic_window(ax, cx, cy, w, h, fill="white", inv="black"):
    """Gothic arched window with cross-bar tracery."""
    hw = w / 2
    # arch radius = half the window width
    arch_r = hw
    straight_h = h - arch_r

    # window outline — rectangle + semicircle arch top
    rect_pts = np.array([
        [cx - hw, cy - h / 2],
        [cx + hw, cy - h / 2],
        [cx + hw, cy - h / 2 + straight_h],
        [cx - hw, cy - h / 2 + straight_h],
    ])
    ax.add_patch(Polygon(rect_pts, closed=True, facecolor=fill, edgecolor="none"))
    # arch top (semicircle)
    theta = np.linspace(0, np.pi, 60)
    arch_cx = cx
    arch_cy = cy - h / 2 + straight_h
    arch_pts = np.column_stack([
        arch_cx + arch_r * np.cos(theta),
        arch_cy + arch_r * np.sin(theta)
    ])
    arch_pts = np.vstack([[arch_cx - arch_r, arch_cy], arch_pts,
                           [arch_cx + arch_r, arch_cy]])
    ax.add_patch(Polygon(arch_pts, closed=True, facecolor=fill, edgecolor="none"))

    # frame border (inv colour)
    frame_w = w * 0.08
    # vertical centre bar
    ax.plot([cx, cx], [cy - h/2 + frame_w, cy - h/2 + straight_h],
            color=inv, linewidth=frame_w * (SIZE/DPI) * 0.35)
    # horizontal bar at 1/3 up
    bar_y = cy - h/2 + straight_h * 0.42
    ax.plot([cx - hw + frame_w, cx + hw - frame_w], [bar_y, bar_y],
            color=inv, linewidth=frame_w * (SIZE/DPI) * 0.30)
    # outer border
    ax.add_patch(Polygon(rect_pts, closed=True, facecolor="none",
                         edgecolor=inv, linewidth=0.9))
    ax.add_patch(Polygon(arch_pts, closed=True, facecolor="none",
                         edgecolor=inv, linewidth=0.9))

    # gothic tracery in arch — two smaller pointed arches
    small_r = arch_r * 0.44
    for sx in (-hw * 0.38, hw * 0.38):
        sub_cx = cx + sx
        sub_cy = arch_cy
        t = np.linspace(0, np.pi, 30)
        sp = np.column_stack([sub_cx + small_r * np.cos(t),
                               sub_cy + small_r * np.sin(t)])
        ax.plot(sp[:, 0], sp[:, 1], color=inv, linewidth=0.65)


def draw():
    """Seamless gothic window grid on black — 4×6 arched windows with tracery."""
    fig, ax = setup_ax()
    cols, rows = 4, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    w = dx * 0.74
    h = dy * 0.88
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                gothic_window(ax, cx + ox, cy + oy, w, h)
    save(fig, "abstract halloween tessellation haunted gothic window pane arch grid pattern black white texture")


if __name__ == "__main__":
    draw()
