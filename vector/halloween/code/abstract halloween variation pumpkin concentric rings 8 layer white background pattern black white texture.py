import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon
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


def draw_pumpkin_core(ax, cx, cy, s):
    """Black jack-o'-lantern face on white background."""
    for lobe_ox in (-s * 0.22, 0, s * 0.22):
        ax.add_patch(Ellipse((cx + lobe_ox, cy), s * 0.56, s * 0.74,
                             facecolor="black", edgecolor="none"))
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.055, cy + s * 0.35), s * 0.11, s * 0.17,
        boxstyle=f"round,pad=0,rounding_size={s*0.03:.4f}",
        facecolor="black", edgecolor="none"))

    # Triangle eyes
    for sign in (-1, 1):
        eye = np.array([
            [cx + sign * s * 0.24, cy + s * 0.14],
            [cx + sign * s * 0.35, cy - s * 0.04],
            [cx + sign * s * 0.13, cy - s * 0.04],
        ])
        ax.add_patch(Polygon(eye, closed=True, facecolor="white", edgecolor="none"))

    # Jagged mouth
    teeth_x = np.linspace(cx - s * 0.28, cx + s * 0.28, 7)
    mouth_pts = [(teeth_x[0], cy - s * 0.10)]
    for k, x in enumerate(teeth_x):
        mouth_pts.append((x, cy - s * 0.25 if k % 2 == 0 else cy - s * 0.10))
    mouth_pts.append((teeth_x[-1], cy - s * 0.10))
    ax.add_patch(Polygon(mouth_pts, closed=True, facecolor="white", edgecolor="none"))


def draw_ring(ax, cx, cy, s, scale, lw=1.0):
    """Single outline ring shaped like a pumpkin body."""
    for lobe_ox in (-s * 0.22 * scale, 0, s * 0.22 * scale):
        ax.add_patch(Ellipse((cx + lobe_ox, cy), s * 0.56 * scale, s * 0.74 * scale,
                             facecolor="none", edgecolor="black", linewidth=lw))


def draw():
    """4×3 grid of pumpkin with 8 concentric outline rings, black on white.
    Rings fade in linewidth outward for a radiating pulse effect.
    """
    fig, ax = setup_ax()
    cols, rows = 4, 3
    dx, dy = PERIOD / cols, PERIOD / rows
    s_core = min(dx, dy) * 0.36

    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                # 8 radiating rings from outermost inward
                for i in range(8, 0, -1):
                    scale = 1.0 + i * 0.20
                    lw = max(1.2 - i * 0.10, 0.3)
                    draw_ring(ax, cx + ox, cy + oy, s_core, scale, lw)
                draw_pumpkin_core(ax, cx + ox, cy + oy, s_core)

    save(fig,
         "abstract halloween variation pumpkin concentric rings 8 layer "
         "white background pattern black white texture")


if __name__ == "__main__":
    draw()
