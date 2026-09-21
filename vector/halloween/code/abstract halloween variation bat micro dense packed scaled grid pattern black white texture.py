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
    print(f"Saved: {jpg_path} | {svg_path}")


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


def draw():
    """Micro-dense bat grid on black — tiny bats packed in a tight 14x18 grid,
    alternating white fill and outline-only for a layered density effect."""
    fig, ax = setup_ax()
    cols, rows = 14, 18
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.38   # significantly smaller than base tessellation
    for row in range(rows):
        for col in range(cols):
            # stagger every other row
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            fill = "white" if (row + col) % 2 == 0 else "none"
            edge = "none" if fill == "white" else "white"
            lw = 0.0 if fill == "white" else 0.6
            for ox, oy in WRAPS:
                ax.add_patch(Polygon(bat_poly(cx + ox, cy + oy, s), closed=True,
                                     facecolor=fill, edgecolor=edge, linewidth=lw))
                if fill == "white":
                    # tiny eye dots
                    ax.add_patch(Circle((cx + ox - 0.3 * s, cy + oy + 0.22 * s),
                                        0.08 * s, facecolor="black", edgecolor="none"))
                    ax.add_patch(Circle((cx + ox + 0.3 * s, cy + oy + 0.22 * s),
                                        0.08 * s, facecolor="black", edgecolor="none"))
    save(fig, "abstract halloween variation bat micro dense packed scaled grid pattern black white texture")


if __name__ == "__main__":
    draw()
