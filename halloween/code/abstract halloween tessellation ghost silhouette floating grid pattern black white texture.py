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


def ghost(ax, cx, cy, s, fill="white", inv="black"):
    """Classic ghost silhouette: dome head + wavy skirt bottom."""
    # dome head
    head_r = s * 0.36
    body_h = s * 0.52
    body_w = s * 0.70

    # body rectangle below dome
    ax.add_patch(Ellipse((cx, cy + s * 0.04), body_w, body_h,
                         facecolor=fill, edgecolor="none"))
    # dome on top
    theta = np.linspace(0, np.pi, 60)
    dome_pts = np.column_stack([
        cx + head_r * 1.0 * np.cos(theta),
        cy + s * 0.04 + head_r * np.sin(theta) + body_h * 0.25
    ])
    dome_pts = np.vstack([
        [cx - head_r, cy + s * 0.04 + body_h * 0.25],
        dome_pts,
        [cx + head_r, cy + s * 0.04 + body_h * 0.25]
    ])
    ax.add_patch(Polygon(dome_pts, closed=True, facecolor=fill, edgecolor="none"))

    # wavy skirt at bottom — 4 bumps
    bottom_y = cy + s * 0.04 - body_h * 0.47
    n_bumps = 4
    half_w = body_w * 0.5
    xs = np.linspace(cx - half_w, cx + half_w, 200)
    # sinusoidal wave drooping down
    wave_amp = s * 0.10
    wave_y = bottom_y - wave_amp * 0.5 - wave_amp * np.sin(
        (xs - cx + half_w) / (body_w) * n_bumps * np.pi
    )
    skirt_pts = [(cx - half_w, bottom_y)]
    skirt_pts += list(zip(xs, wave_y))
    skirt_pts += [(cx + half_w, bottom_y)]
    ax.add_patch(Polygon(skirt_pts, closed=True, facecolor=fill, edgecolor="none"))

    # eyes
    for ex in (-s * 0.14, s * 0.14):
        ax.add_patch(Ellipse((cx + ex, cy + s * 0.26), s * 0.11, s * 0.14,
                             facecolor=inv, edgecolor="none"))
    # open "o" mouth
    ax.add_patch(Circle((cx, cy + s * 0.10), s * 0.075,
                        facecolor=inv, edgecolor="none"))


def draw():
    """Seamless floating ghost tessellation on black, 6x7 staggered grid."""
    fig, ax = setup_ax()
    cols, rows = 6, 7
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.82
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                ghost(ax, cx + ox, cy + oy, s)
    save(fig, "abstract halloween tessellation ghost silhouette floating grid pattern black white texture")


if __name__ == "__main__":
    draw()
