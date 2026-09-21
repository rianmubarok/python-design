import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon
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


def leaf(ax, cx, cy, size, angle_deg):
    """A simple oval leaf."""
    a = np.radians(angle_deg)
    # Leaf as a narrow ellipse rotated
    pts = []
    n = 40
    for i in range(n):
        t = 2 * np.pi * i / n
        lx = cx + size * 0.28 * np.cos(t)
        ly = cy + size * 0.12 * np.sin(t)
        # rotate
        rx = lx * np.cos(a) - ly * np.sin(a) + cx * (1 - np.cos(a)) + cy * np.sin(a)
        ry = lx * np.sin(a) + ly * np.cos(a) - cx * np.sin(a) + cy * (1 - np.cos(a))
        pts.append([rx, ry])
    ax.add_patch(Polygon(pts, closed=True, facecolor="black", edgecolor="none"))
    # midvein
    vx0 = cx + size * 0.24 * np.cos(a + np.pi)
    vy0 = cy + size * 0.24 * np.sin(a + np.pi)
    vx1 = cx + size * 0.24 * np.cos(a)
    vy1 = cy + size * 0.24 * np.sin(a)
    ax.plot([vx0, vx1], [vy0, vy1], color="white", linewidth=0.5)


def tendril(ax, cx, cy, dx, dy, n_coils=2):
    """A coiling vine tendril from (cx,cy) toward (cx+dx, cy+dy)."""
    t = np.linspace(0, n_coils * 2 * np.pi, 120)
    coil_r = 1.5
    decay = np.exp(-t / (n_coils * 2 * np.pi) * 1.5)
    main_x = np.linspace(cx, cx + dx, 120)
    main_y = np.linspace(cy, cy + dy, 120)
    perp_x = -dy / np.hypot(dx, dy + 1e-9)
    perp_y = dx / np.hypot(dx, dy + 1e-9)
    xs = main_x + coil_r * decay * np.cos(t) * perp_x
    ys = main_y + coil_r * decay * np.cos(t) * perp_y
    ax.plot(xs, ys, color="black", linewidth=0.75)


def pumpkin_body(ax, cx, cy, s):
    """Pumpkin body only (no face) — just ribbed round shape."""
    for ox in (-s * 0.24, 0, s * 0.24):
        ax.add_patch(Ellipse((cx + ox, cy), s * 0.60, s * 0.76,
                             facecolor="black", edgecolor="none"))
    for ox in (-s * 0.24, 0, s * 0.24):
        ax.plot([cx + ox, cx + ox], [cy - s * 0.37, cy + s * 0.37],
                color="white", linewidth=0.8, solid_capstyle="round")
    # stem
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.06, cy + s * 0.37), s * 0.12, s * 0.18,
        boxstyle=f"round,pad=0,rounding_size={s*0.04:.4f}",
        facecolor="black", edgecolor="none"))


def draw():
    """Pumpkins connected by curling vines and leaves — an organic seamless tiling
    where vines grow between each pumpkin node in a hex-like grid."""
    fig, ax = setup_ax()
    cols, rows = 4, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.52
    # Vine directions between cells
    vine_offsets = [(dx, 0), (dx * 0.5, dy), (-dx * 0.5, dy)]
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                # vines towards neighbours
                for vdx, vdy in vine_offsets:
                    tendril(ax, cx + ox, cy + oy, vdx * 0.82, vdy * 0.82, n_coils=1)
                    # leaf along vine
                    leaf(ax, cx + ox + vdx * 0.45, cy + oy + vdy * 0.45,
                         s * 0.4, np.degrees(np.arctan2(vdy, vdx)) + 45)
                # pumpkin
                pumpkin_body(ax, cx + ox, cy + oy, s)
    save(fig, "abstract halloween variation pumpkin stem vine organic tiling pattern black white texture")


if __name__ == "__main__":
    draw()
