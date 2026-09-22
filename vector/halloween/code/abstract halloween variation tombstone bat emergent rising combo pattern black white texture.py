import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Ellipse
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


def tombstone(ax, cx, cy, w, h, fill="white"):
    """Classic rounded-top tombstone."""
    inv = "black" if fill == "white" else "white"
    body_h = h * 0.62
    arch_r = w * 0.5
    # rectangular body
    ax.add_patch(FancyBboxPatch(
        (cx - w * 0.5, cy - h * 0.5), w, body_h,
        boxstyle="square,pad=0",
        facecolor=fill, edgecolor="none"))
    # arched top as semicircle
    theta = np.linspace(0, np.pi, 50)
    arch_pts = list(zip(
        cx + arch_r * np.cos(theta),
        cy - h * 0.5 + body_h + arch_r * np.sin(theta)
    ))
    arch_pts = [(cx - w * 0.5, cy - h * 0.5 + body_h)] + arch_pts + \
               [(cx + w * 0.5, cy - h * 0.5 + body_h)]
    ax.add_patch(Polygon(arch_pts, closed=True, facecolor=fill, edgecolor="none"))
    # RIP text substitute — two horizontal lines
    line_y1 = cy - h * 0.5 + body_h * 0.72
    line_y2 = cy - h * 0.5 + body_h * 0.58
    for ly in (line_y1, line_y2):
        ax.plot([cx - w * 0.28, cx + w * 0.28], [ly, ly],
                color=inv, linewidth=0.55)
    # crack line
    crack = [(cx + w * 0.06, cy - h * 0.5 + body_h * 0.30),
             (cx + w * 0.14, cy - h * 0.5 + body_h * 0.14),
             (cx + w * 0.09, cy - h * 0.5 + body_h * 0.02)]
    ax.plot([p[0] for p in crack], [p[1] for p in crack],
            color=inv, linewidth=0.5)


def tombstone_bat_unit(ax, cx, cy, tw, th, bat_s, rng):
    """One tombstone + bat rising from behind the top."""
    tombstone(ax, cx, cy, tw, th, fill="white")
    # bat perched just above tombstone top
    top_y = cy - th * 0.5 + th * 0.62 + tw * 0.5 + bat_s * 0.15
    angle = rng.uniform(-0.25, 0.25)
    ax.add_patch(Polygon(bat_poly(cx, top_y, bat_s, angle),
                         closed=True, facecolor="white", edgecolor="none"))


def draw():
    """5×4 staggered grid of tombstone+bat emergent units on black background."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(7)
    cols, rows = 5, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    tw = dx * 0.62
    th = dy * 0.70
    bat_s = tw * 0.36

    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                tombstone_bat_unit(ax, cx + ox, cy + oy, tw, th, bat_s, rng)

    save(fig, "abstract halloween variation tombstone bat emergent rising combo pattern black white texture")


if __name__ == "__main__":
    draw()
