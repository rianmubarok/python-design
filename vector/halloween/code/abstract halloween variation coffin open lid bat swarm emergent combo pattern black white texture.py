import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Ellipse
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI  = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR  = SCRIPT_DIR.parent / "output"
JPG_DIR     = OUTPUT_DIR / "jpg"
SVG_DIR     = OUTPUT_DIR / "svg"
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


def draw_coffin(ax, cx, cy, w, h, fill="black"):
    """Classic hexagonal coffin silhouette (wider at shoulders, tapered at feet)."""
    hw, hh = w * 0.5, h * 0.5
    # Point order: top-centre, shoulder-right, hip-right, foot-right, foot-left, hip-left, shoulder-left
    pts = [
        (cx,           cy + hh * 1.00),   # top crown centre
        (cx + hw*0.60, cy + hh * 0.70),   # top-right shoulder
        (cx + hw*1.00, cy + hh * 0.30),   # right shoulder
        (cx + hw*1.00, cy - hh * 0.30),   # right waist
        (cx + hw*0.70, cy - hh * 1.00),   # bottom-right foot
        (cx - hw*0.70, cy - hh * 1.00),   # bottom-left foot
        (cx - hw*1.00, cy - hh * 0.30),   # left waist
        (cx - hw*1.00, cy + hh * 0.30),   # left shoulder
        (cx - hw*0.60, cy + hh * 0.70),   # top-left shoulder
    ]
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor="none"))

    # Interior void (coffin opening) — slightly smaller, white
    inv = "white" if fill == "black" else "black"
    inset = 0.12
    inner_pts = [(x + (cx - x) * inset, y + (cy - y) * inset) for x, y in pts]
    ax.add_patch(Polygon(inner_pts, closed=True, facecolor=inv, edgecolor="none"))


def draw_tiny_bat(ax, cx, cy, s, fill="black"):
    """Tiny simple bat: body ellipse + two wing triangles."""
    ax.add_patch(Ellipse((cx, cy), s * 0.25, s * 0.16,
                         facecolor=fill, edgecolor="none"))
    for sign in (-1, 1):
        wing = [
            (cx, cy + s * 0.04),
            (cx + sign * s * 0.44, cy + s * 0.08),
            (cx + sign * s * 0.44, cy - s * 0.10),
            (cx + sign * s * 0.18, cy - s * 0.14),
        ]
        ax.add_patch(Polygon(wing, closed=True, facecolor=fill, edgecolor="none"))


def draw_tile(ax, cx, cy, r, seed=0):
    """Coffin with a swarm of bats rising out of it in an expanding arc."""
    rng = np.random.default_rng(seed)

    coffin_w = r * 0.62
    coffin_h = r * 0.90
    coffin_cy = cy - r * 0.12
    draw_coffin(ax, cx, coffin_cy, coffin_w, coffin_h)

    # Bats emerge upward from coffin opening
    n_bats = 7
    for i in range(n_bats):
        t = (i + 1) / (n_bats + 1)   # 0..1 along arc
        # Spread out horizontally as they rise
        bx = cx + (t - 0.5) * 2.0 * r * 0.55 * rng.uniform(0.7, 1.3)
        # Rise upward, highest bat near edge, loose curve
        rise = coffin_cy + coffin_h * 0.48 + t * r * 0.70 * rng.uniform(0.8, 1.2)
        bat_s = r * 0.10 * (1.0 - t * 0.45)  # shrink with distance
        draw_tiny_bat(ax, bx, rise, bat_s, fill="black")


def draw():
    """3×4 grid of coffin + bat swarm tiles. White background."""
    fig, ax = setup_ax()
    cols, rows = 3, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    r = min(dx, dy) * 0.46

    for row in range(rows):
        shift = dx * 0.5 if row % 2 else 0.0
        for col in range(cols):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            seed = row * cols + col
            for ox, oy in WRAPS:
                draw_tile(ax, cx + ox, cy + oy, r, seed=seed)

    save(fig,
         "abstract halloween variation coffin open lid bat swarm emergent "
         "combo pattern black white texture")


if __name__ == "__main__":
    draw()
