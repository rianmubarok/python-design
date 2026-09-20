import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon
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


def potion_bottle(ax, cx, cy, s, fill="black", inv="white"):
    """Potion bottle: round bulb body + narrow neck + cork + liquid level + skull label."""
    bw = s * 0.56   # body width
    bh = s * 0.58   # body height
    neck_w = s * 0.20
    neck_h = s * 0.28
    body_bot = cy - s * 0.42
    body_cen = cy - s * 0.14
    neck_bot = body_cen + bh * 0.44
    neck_top = neck_bot + neck_h

    # round body
    ax.add_patch(Ellipse((cx, body_cen), bw, bh, facecolor=fill, edgecolor="none"))

    # neck
    ax.add_patch(FancyBboxPatch(
        (cx - neck_w / 2, neck_bot - s * 0.01), neck_w, neck_h + s * 0.01,
        boxstyle=f"round,pad=0,rounding_size={s*0.03:.4f}",
        facecolor=fill, edgecolor="none"))

    # cork / stopper
    ax.add_patch(FancyBboxPatch(
        (cx - neck_w / 2 - s * 0.04, neck_top), neck_w + s * 0.08, s * 0.12,
        boxstyle=f"round,pad=0,rounding_size={s*0.04:.4f}",
        facecolor=fill, edgecolor="none"))

    # liquid level line inside body
    liq_y = body_cen - bh * 0.05
    half_chord = np.sqrt(max(0, (bw / 2) ** 2 - (liq_y - body_cen) ** 2)) * 0.92
    ax.plot([cx - half_chord, cx + half_chord], [liq_y, liq_y],
            color=inv, linewidth=1.0)

    # highlight oval on bottle shoulder
    ax.add_patch(Ellipse((cx - bw * 0.22, body_cen + bh * 0.20),
                         bw * 0.18, bh * 0.12, angle=30,
                         facecolor=inv, edgecolor="none"))

    # small skull face as label
    skull_cx, skull_cy, sk = cx, body_cen - bh * 0.12, s * 0.14
    ax.add_patch(Ellipse((skull_cx, skull_cy + sk * 0.1), sk * 0.9, sk * 0.8,
                         facecolor=inv, edgecolor="none"))
    for ex in (-sk * 0.22, sk * 0.22):
        ax.add_patch(Circle((skull_cx + ex, skull_cy + sk * 0.14), sk * 0.16,
                            facecolor=fill, edgecolor="none"))
    ax.add_patch(Polygon(
        [[skull_cx, skull_cy - sk * 0.02],
         [skull_cx - sk * 0.10, skull_cy - sk * 0.22],
         [skull_cx + sk * 0.10, skull_cy - sk * 0.22]],
        closed=True, facecolor=fill, edgecolor="none"))


def draw():
    """Seamless potion bottle grid, alternating black-on-white and white-on-black."""
    fig, ax = setup_ax()
    cols, rows = 6, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.88
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            fill = "black" if (row + col) % 2 == 0 else "white"
            inv = "white" if fill == "black" else "black"
            bg = "white" if fill == "black" else "black"
            # cell background square
            ax.add_patch(FancyBboxPatch(
                (cx - dx / 2, cy - dy / 2), dx, dy,
                boxstyle="square,pad=0",
                facecolor=bg, edgecolor="none"))
            for ox, oy in WRAPS:
                potion_bottle(ax, cx + ox, cy + oy, s, fill=fill, inv=inv)
    save(fig, "abstract halloween tessellation potion bottle repeating grid pattern black white texture")


if __name__ == "__main__":
    draw()
