import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
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


def crow(ax, cx, cy, s, facing=1):
    """Crow/raven side-profile silhouette. facing=1 right, -1 left."""
    f = facing
    fill = "black"

    # body (elongated ellipse, slightly tilted)
    ax.add_patch(Ellipse((cx, cy), s * 0.62, s * 0.32, angle=-8 * f,
                         facecolor=fill, edgecolor="none"))

    # head
    head_r = s * 0.18
    head_cx = cx + f * s * 0.26
    head_cy = cy + s * 0.14
    ax.add_patch(Ellipse((head_cx, head_cy), head_r * 1.8, head_r * 1.6,
                         facecolor=fill, edgecolor="none"))

    # beak — pointed triangle
    beak_pts = np.array([
        [head_cx + f * head_r * 0.80, head_cy + head_r * 0.05],
        [head_cx + f * head_r * 0.80, head_cy - head_r * 0.25],
        [head_cx + f * head_r * 1.70, head_cy - head_r * 0.05],
    ])
    ax.add_patch(Polygon(beak_pts, closed=True, facecolor=fill, edgecolor="none"))

    # tail — fan shape
    tail_base_x = cx - f * s * 0.28
    tail_base_y = cy - s * 0.04
    for i in range(5):
        angle = np.radians(-160 + i * 14) * f + np.radians(180)
        tl = s * (0.22 + i * 0.02)
        ex = tail_base_x + tl * np.cos(angle)
        ey = tail_base_y + tl * np.sin(angle)
        ax.plot([tail_base_x, ex], [tail_base_y, ey],
                color=fill, linewidth=s * 0.06, solid_capstyle="round")

    # wing fold lines
    wing_x = cx + f * s * 0.05
    for i in range(3):
        wx = wing_x - f * i * s * 0.08
        ax.plot([wx, wx + f * s * 0.10], [cy + s * 0.06, cy - s * 0.06],
                color="white", linewidth=0.5, alpha=0.6)

    # legs — two thin sticks
    for leg_x in (cx - f * s * 0.08, cx + f * s * 0.06):
        ax.plot([leg_x, leg_x + f * s * 0.02], [cy - s * 0.15, cy - s * 0.28],
                color=fill, linewidth=0.8)
        # claws
        for ca in (-25, 0, 25):
            ra = np.radians(270 + ca)
            ax.plot([leg_x + f * s * 0.02,
                     leg_x + f * s * 0.02 + s * 0.06 * np.cos(ra)],
                    [cy - s * 0.28,
                     cy - s * 0.28 + s * 0.06 * np.sin(ra)],
                    color=fill, linewidth=0.6)

    # eye (white dot)
    ax.add_patch(Ellipse((head_cx + f * head_r * 0.20, head_cy + head_r * 0.12),
                         head_r * 0.28, head_r * 0.28,
                         facecolor="white", edgecolor="none"))


def draw():
    """Scattered crow/raven silhouettes — jittered 8×8 grid, alternating facing directions."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(13)
    cols, rows = 8, 8
    dx, dy = PERIOD / cols, PERIOD / rows

    for row in range(rows):
        for col in range(cols):
            jx = rng.uniform(0.10, 0.90) * dx
            jy = rng.uniform(0.10, 0.90) * dy
            cx = col * dx + jx
            cy = row * dy + jy
            s = rng.uniform(0.32, 0.52) * min(dx, dy)
            facing = 1 if (row + col) % 2 == 0 else -1
            for ox, oy in WRAPS:
                crow(ax, cx + ox, cy + oy, s, facing)
    save(fig, "abstract halloween variation raven crow silhouette scatter field pattern black white texture")


if __name__ == "__main__":
    draw()
