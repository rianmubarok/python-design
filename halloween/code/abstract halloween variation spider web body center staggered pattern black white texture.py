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
    print(f"Saved: {jpg_path}")


def web_with_spider(ax, cx, cy, r, twist=0.0):
    spokes = 8
    angles = [k * np.pi / 4 + twist for k in range(spokes)]
    # draw spokes
    for a in angles:
        ax.plot([cx, cx + r * np.cos(a)], [cy, cy + r * np.sin(a)],
                color="black", linewidth=0.7, solid_capstyle="round")
    # concentric rings
    for sc in (0.22, 0.42, 0.63, 0.84):
        pts = np.array([[cx + r * sc * np.cos(a), cy + r * sc * np.sin(a)] for a in angles])
        pts = np.vstack([pts, pts[0]])
        ax.plot(pts[:, 0], pts[:, 1], color="black", linewidth=0.55)

    # spider body at center
    body_r = r * 0.13
    abdomen_r = r * 0.20
    # abdomen (lower oval)
    ax.add_patch(Ellipse((cx, cy - abdomen_r * 0.65), abdomen_r * 1.3, abdomen_r * 1.6,
                         facecolor="black", edgecolor="none"))
    # head (upper circle)
    ax.add_patch(Circle((cx, cy + body_r * 0.3), body_r, facecolor="black", edgecolor="none"))
    # 8 legs
    leg_spread = r * 0.45
    for i, side in enumerate([-1, 1]):
        for j in range(4):
            angle = np.radians(30 + j * 22) * side
            lx = cx + side * body_r
            ly = cy
            ex = cx + side * leg_spread * np.cos(angle)
            ey = cy + leg_spread * np.sin(angle) * 0.6
            mx = (lx + ex) / 2 + side * leg_spread * 0.18
            my = (ly + ey) / 2 + leg_spread * 0.1
            # two-segment leg
            ax.plot([lx, mx], [ly, my], color="black", linewidth=0.9)
            ax.plot([mx, ex], [my, ey], color="black", linewidth=0.9)
    # eyes
    for ex_off in (-body_r * 0.35, body_r * 0.35):
        ax.add_patch(Circle((cx + ex_off, cy + body_r * 0.5), body_r * 0.22,
                            facecolor="white", edgecolor="none"))


def draw():
    """Seamless staggered spider-web grid each with a detailed spider body at center."""
    fig, ax = setup_ax()
    cols, rows = 7, 7
    dx, dy = PERIOD / cols, PERIOD / rows
    r = min(dx, dy) * 0.56
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            twist = np.pi / 8 if (row + col) % 2 else 0.0
            for ox, oy in WRAPS:
                web_with_spider(ax, cx + ox, cy + oy, r, twist)
    save(fig, "abstract halloween variation spider web body center staggered pattern black white texture")


if __name__ == "__main__":
    draw()
