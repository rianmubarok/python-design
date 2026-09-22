import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch
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


def potion_bottle(ax, cx, cy, s):
    """Compact white potion silhouette — no aura, just the bottle shape."""
    body_r = s * 0.34

    ax.add_patch(Circle((cx, cy - s * 0.08), body_r,
                        facecolor="white", edgecolor="none"))
    # Neck
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.08, cy + s * 0.22), s * 0.16, s * 0.22,
        boxstyle="square,pad=0",
        facecolor="white", edgecolor="none"))
    # Cork
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.10, cy + s * 0.42), s * 0.20, s * 0.07,
        boxstyle=f"round,pad=0,rounding_size={s*0.018:.4f}",
        facecolor="white", edgecolor="none"))
    # Skull label (black on white body)
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.15, cy - s * 0.20), s * 0.30, s * 0.18,
        boxstyle=f"round,pad=0,rounding_size={s*0.018:.4f}",
        facecolor="black", edgecolor="none"))
    # Tiny skull eyes
    sr = s * 0.035
    ax.add_patch(Circle((cx, cy - s * 0.09), sr, facecolor="white", edgecolor="none"))
    for ex in (-sr * 0.45, sr * 0.45):
        ax.add_patch(Circle((cx + ex, cy - s * 0.09), sr * 0.30,
                            facecolor="black", edgecolor="none"))

    # Small bubble dots (no aura ring)
    for (bx, by, br) in [(-0.14, -0.01, 0.032), (0.12, 0.08, 0.025)]:
        ax.add_patch(Circle((cx + bx * s, cy + by * s), br * s,
                            facecolor="none", edgecolor="white", linewidth=0.6))


def draw():
    """Dense 7×5 grid of micro potion bottles, packed tight with no aura rings.
    Staggered rows for hex-like density. White bottles on black background.
    """
    fig, ax = setup_ax()
    cols, rows = 7, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.48

    for row in range(rows):
        shift = dx * 0.5 if row % 2 else 0.0
        for col in range(cols):
            cx = (col + 0.5) * dx + shift
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    potion_bottle(ax, px, py, s)

    save(fig,
         "abstract halloween variation potion bottle micro dense packed no aura "
         "pattern black white texture")


if __name__ == "__main__":
    draw()
