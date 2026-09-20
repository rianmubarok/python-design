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
    print(f"Saved: {jpg_path} | {svg_path}")


def cauldron(ax, cx, cy, s, fill="black", inv="white"):
    """Witch cauldron silhouette: round pot, legs, rim, handle."""
    pot_w = s * 0.80
    pot_h = s * 0.60
    pot_cy = cy - s * 0.05

    # pot body (round trapezoid — wider at top)
    pts = np.array([
        [-pot_w * 0.42, -pot_h * 0.50],   # bottom-left
        [ pot_w * 0.42, -pot_h * 0.50],   # bottom-right
        [ pot_w * 0.50,  pot_h * 0.48],   # top-right
        [-pot_w * 0.50,  pot_h * 0.48],   # top-left
    ]) + [cx, pot_cy]
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor="none"))

    # round bottom
    ax.add_patch(Ellipse((cx, pot_cy - pot_h * 0.50 + pot_w * 0.22),
                         pot_w * 0.84, pot_w * 0.44,
                         facecolor=fill, edgecolor="none"))

    # rim at top
    ax.add_patch(Ellipse((cx, pot_cy + pot_h * 0.48),
                         pot_w * 1.02, pot_h * 0.15,
                         facecolor=fill, edgecolor="none"))

    # three legs
    for lx in (-s * 0.24, 0, s * 0.24):
        ax.add_patch(FancyBboxPatch(
            (cx + lx - s * 0.035, pot_cy - pot_h * 0.50 - s * 0.18),
            s * 0.07, s * 0.20,
            boxstyle=f"round,pad=0,rounding_size={s*0.025:.4f}",
            facecolor=fill, edgecolor="none"))

    # handle arc
    ax.add_patch(Ellipse((cx, pot_cy + pot_h * 0.55), pot_w * 0.58, pot_h * 0.50,
                         facecolor="none", edgecolor=fill, linewidth=s * 0.04 * (SIZE/DPI) * 0.05))

    # brew surface inside rim (inv colour)
    ax.add_patch(Ellipse((cx, pot_cy + pot_h * 0.44),
                         pot_w * 0.88, pot_h * 0.12,
                         facecolor=inv, edgecolor="none"))


def bubble(ax, cx, cy, r, fill="black"):
    """A single bubble with highlight ring."""
    ax.add_patch(Circle((cx, cy), r, facecolor=fill, edgecolor="none"))
    ax.add_patch(Circle((cx + r * 0.28, cy + r * 0.28), r * 0.20,
                        facecolor="none",
                        edgecolor="white" if fill == "black" else "black",
                        linewidth=0.4, alpha=0.6))


def draw():
    """4×5 grid — each tile: cauldron silhouette with cluster of rising bubbles above."""
    fig, ax = setup_ax()
    rng = np.random.default_rng(55)
    cols, rows = 4, 5
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.72
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy - s * 0.08
            fill = "black" if (row + col) % 2 == 0 else "white"
            inv = "white" if fill == "black" else "black"
            bg = inv
            ax.add_patch(Polygon([
                [cx-dx/2, cy-dy/2],[cx+dx/2, cy-dy/2],
                [cx+dx/2, cy+dy/2],[cx-dx/2, cy+dy/2]
            ], closed=True, facecolor=bg, edgecolor="none"))
            for ox, oy in WRAPS:
                cauldron(ax, cx+ox, cy+oy, s, fill=fill, inv=inv)
                # bubbles rising from brew surface
                brew_y = cy + oy + s * 0.40
                n_b = rng.integers(4, 8)
                for _ in range(n_b):
                    bx = cx + ox + rng.uniform(-s*0.30, s*0.30)
                    by = brew_y + rng.uniform(s*0.02, s*0.40)
                    br = rng.uniform(s*0.028, s*0.072)
                    bubble(ax, bx, by, br, fill=fill)
    save(fig, "abstract halloween tessellation witch cauldron bubble cluster pattern black white texture")


if __name__ == "__main__":
    draw()
