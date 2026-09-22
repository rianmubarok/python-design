import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse
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


def draw_web_on_brim(ax, cx, brim_cy, brim_rx, brim_ry, lw=0.6):
    """Draw half-circle spider web that drapes across the hat brim."""
    n_spokes = 9
    n_rings = 4
    # Web anchored at brim centre, spreading downward
    web_cx = cx
    web_cy = brim_cy
    max_r = brim_rx * 0.95

    for k in range(n_spokes):
        # Spokes fan out downward (angle range π to 2π = lower half circle)
        a = np.pi + k * np.pi / (n_spokes - 1)
        ax.plot([web_cx, web_cx + max_r * np.cos(a)],
                [web_cy, web_cy + max_r * 0.55 * np.sin(a)],
                color="white", linewidth=lw, zorder=4, alpha=0.75)

    for r_i in range(1, n_rings + 1):
        r = max_r * r_i / n_rings
        t = np.linspace(np.pi, 2 * np.pi, 60)
        ax.plot(web_cx + r * np.cos(t), web_cy + r * 0.55 * np.sin(t),
                color="white", linewidth=lw * 0.8, zorder=4, alpha=0.70)


def draw_hat_with_web_brim(ax, cx, cy, s, fill="white"):
    """Witch hat (solid fill) with a spiderweb lace overlay on the brim."""
    # Cone
    cone = np.array([
        [cx,            cy + s * 0.46],
        [cx - s * 0.15, cy - s * 0.06],
        [cx + s * 0.15, cy - s * 0.06],
    ])
    ax.add_patch(Polygon(cone, closed=True, facecolor=fill, edgecolor="none", zorder=2))

    # Brim ellipse
    brim_cy = cy - s * 0.03
    brim_rx = s * 0.40
    brim_ry = s * 0.105
    ax.add_patch(Ellipse((cx, brim_cy), brim_rx * 2, brim_ry * 2,
                         facecolor=fill, edgecolor="none", zorder=2))

    # Band
    ax.add_patch(Ellipse((cx, cy + s * 0.04), s * 0.185, s * 0.05,
                         facecolor="black" if fill == "white" else "white",
                         edgecolor="none", zorder=3))

    # Spider-web lace draped from brim downward
    draw_web_on_brim(ax, cx, brim_cy, brim_rx, brim_ry, lw=0.8)


def draw():
    """4×5 staggered grid. White witch hats on black, each with a spider-web
    lace pattern draped over the brim — like hanging lace trim."""
    fig, ax = setup_ax()

    cols, rows = 4, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.76

    for row in range(-1, rows + 1):
        shift = (dx * 0.5) if row % 2 else 0.0
        for col in range(-1, cols + 2):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    draw_hat_with_web_brim(ax, px, py, s, fill="white")

    save(fig, "abstract halloween variation witch hat spider web brim lace overlay pattern black white texture")


if __name__ == "__main__":
    draw()
