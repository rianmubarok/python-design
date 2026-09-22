import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Polygon
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


def draw_tombstone(ax, cx, cy, w, h, fill="black", zorder=1):
    """Classic tombstone: rounded arch top, rectangular body."""
    r = w * 0.5  # arch radius = half-width
    # Body rect
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h * 0.65,
        boxstyle="square,pad=0",
        facecolor=fill, edgecolor="none", zorder=zorder))
    # Rounded arch top
    t = np.linspace(0, np.pi, 40)
    arch_x = cx + r * np.cos(t)
    arch_y = cy + h * 0.15 + r * np.sin(t)
    body_pts = np.array([
        [cx - r, cy + h * 0.15],
        *zip(arch_x, arch_y),
        [cx + r, cy + h * 0.15],
    ])
    ax.add_patch(Polygon(body_pts, closed=True,
                         facecolor=fill, edgecolor="none", zorder=zorder))


def draw():
    """Overlapping tombstones at 4 size scales, scattered via fixed RNG.
    Largest drawn first (back), smallest last (front) — depth illusion.
    Black on white background; overlapping creates layered graveyard silhouette."""
    fig, ax = setup_ax()

    rng = np.random.default_rng(13)
    layers = [
        dict(n=6,  s_min=12.0, s_max=18.0, y_band=(0.55, 0.75)),
        dict(n=8,  s_min=8.0,  s_max=13.0, y_band=(0.38, 0.60)),
        dict(n=10, s_min=5.0,  s_max=9.0,  y_band=(0.22, 0.45)),
        dict(n=14, s_min=3.0,  s_max=6.0,  y_band=(0.10, 0.30)),
    ]

    all_stones = []
    for z, layer in enumerate(layers):
        xs = rng.uniform(0, PERIOD, layer['n'])
        ys_frac = rng.uniform(layer['y_band'][0], layer['y_band'][1], layer['n'])
        szs = rng.uniform(layer['s_min'], layer['s_max'], layer['n'])
        for xi, yf, sz in zip(xs, ys_frac, szs):
            all_stones.append(dict(
                cx=xi, cy=yf * PERIOD, w=sz * 0.65, h=sz, zorder=z + 1))

    # Sort by y (lower = closer = drawn on top)
    all_stones.sort(key=lambda s: s['cy'], reverse=True)

    for stone in all_stones:
        cx, cy, w, h, z = stone['cx'], stone['cy'], stone['w'], stone['h'], stone['zorder']
        for ox, oy in WRAPS:
            px, py = cx + ox, cy + oy
            if -20 <= px <= PERIOD + 20 and -20 <= py <= PERIOD + 20:
                draw_tombstone(ax, px, py, w, h, fill="black", zorder=z)

    save(fig, "abstract halloween variation tombstone scale gradient overlapping silhouette field pattern black white texture")


if __name__ == "__main__":
    draw()
