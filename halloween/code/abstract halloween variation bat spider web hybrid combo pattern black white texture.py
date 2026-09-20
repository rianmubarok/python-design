import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
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


def bat_poly(cx, cy, s):
    pts = np.array([
        [0.00, 0.08], [0.12, 0.18], [0.10, 0.05], [0.42, 0.22], [0.78, 0.38],
        [0.62, 0.08], [0.95, 0.12], [0.55, -0.08], [0.72, -0.28], [0.28, -0.10],
        [0.18, -0.22], [0.08, -0.08], [0.00, -0.18],
        [-0.08, -0.08], [-0.18, -0.22], [-0.28, -0.10], [-0.72, -0.28],
        [-0.55, -0.08], [-0.95, 0.12], [-0.62, 0.08], [-0.78, 0.38],
        [-0.42, 0.22], [-0.10, 0.05], [-0.12, 0.18],
    ])
    return pts * s + [cx, cy]


def mini_web(ax, cx, cy, r):
    """Faint spiderweb behind the bat cell."""
    spokes = 6
    for k in range(spokes):
        a = k * np.pi / 3
        ax.plot([cx, cx + r * np.cos(a)], [cy, cy + r * np.sin(a)],
                color="white", linewidth=0.35, alpha=0.45)
    for sc in (0.3, 0.60, 0.90):
        pts = np.array([[cx + r * sc * np.cos(k * np.pi / 3),
                         cy + r * sc * np.sin(k * np.pi / 3)] for k in range(spokes)])
        pts = np.vstack([pts, pts[0]])
        ax.plot(pts[:, 0], pts[:, 1], color="white", linewidth=0.3, alpha=0.45)


def draw():
    """Bat silhouettes on an underlying spider-web lattice — bats fill the nodes,
    webs fill the background space. Black background with white motifs."""
    fig, ax = setup_ax()
    cols, rows = 7, 8
    dx, dy = PERIOD / cols, PERIOD / rows
    cell_r = min(dx, dy) * 0.55
    bat_s = min(dx, dy) * 0.40
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                mini_web(ax, cx + ox, cy + oy, cell_r)
                ax.add_patch(Polygon(bat_poly(cx + ox, cy + oy, bat_s),
                                     closed=True, facecolor="white", edgecolor="none"))
                ax.add_patch(Circle((cx + ox - 0.3 * bat_s, cy + oy + 0.22 * bat_s),
                                    0.06 * bat_s, facecolor="black", edgecolor="none"))
                ax.add_patch(Circle((cx + ox + 0.3 * bat_s, cy + oy + 0.22 * bat_s),
                                    0.06 * bat_s, facecolor="black", edgecolor="none"))
    save(fig, "abstract halloween variation bat spider web hybrid combo pattern black white texture")


if __name__ == "__main__":
    draw()
