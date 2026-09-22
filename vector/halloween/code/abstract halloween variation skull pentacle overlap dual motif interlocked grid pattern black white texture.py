import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon, Circle, PathPatch
from matplotlib.path import Path as MPath
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


def draw_pentacle(ax, cx, cy, r, lw=1.2, color="black"):
    """5-pointed star (pentacle) outline only."""
    angles = [np.pi/2 + k * 4 * np.pi / 5 for k in range(5)]
    pts = [(cx + r * np.cos(a), cy + r * np.sin(a)) for a in angles]
    # Draw the 5 lines of the star (connecting every 2nd vertex)
    for i in range(5):
        p1 = pts[i]
        p2 = pts[(i + 2) % 5]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                color=color, linewidth=lw, zorder=2)
    # Outer circle
    t = np.linspace(0, 2 * np.pi, 100)
    ax.plot(cx + r * np.cos(t), cy + r * np.sin(t),
            color=color, linewidth=lw * 0.7, zorder=2, alpha=0.55)


def skull(ax, cx, cy, s, fill="black"):
    inv = "white" if fill == "black" else "black"
    edge = "none" if fill == "black" else "black"
    elw = 0.0 if fill == "black" else s * 0.07
    skull_cy = cy + 0.08 * s
    ax.add_patch(Ellipse((cx, skull_cy + 0.09*s), 0.72*s, 0.62*s,
                         facecolor=fill, edgecolor=edge, linewidth=elw, zorder=3))
    ax.add_patch(FancyBboxPatch(
        (cx - 0.22*s, skull_cy - 0.22*s), 0.44*s, 0.18*s,
        boxstyle=f"round,pad=0,rounding_size={0.035*s:.4f}",
        facecolor=fill, edgecolor=edge, linewidth=elw, zorder=3))
    for ex in (-0.155*s, 0.155*s):
        ax.add_patch(Ellipse((cx+ex, skull_cy+0.13*s), 0.16*s, 0.18*s,
                             facecolor=inv, edgecolor="none", zorder=4))
    ax.add_patch(Polygon(
        [[cx, skull_cy+0.01*s], [cx-0.055*s, skull_cy-0.075*s],
         [cx+0.055*s, skull_cy-0.075*s]],
        closed=True, facecolor=inv, edgecolor="none", zorder=4))
    for tx in (-0.095*s, 0.0, 0.095*s):
        ax.add_patch(FancyBboxPatch(
            (cx+tx-0.022*s, skull_cy-0.185*s), 0.044*s, 0.085*s,
            boxstyle="round,pad=0,rounding_size=0.003",
            facecolor=inv, edgecolor="none", zorder=4))


def draw():
    """Checkerboard: black cells hold a small pentacle outline,
    white cells hold a solid black skull. The two motifs interlock.
    Creates a high-contrast dual-motif grid on white background."""
    fig, ax = setup_ax()

    n = 5  # 5×5 grid
    d = PERIOD / n
    r_pent = d * 0.38
    s_skull = d * 0.50

    for row in range(-1, n + 1):
        for col in range(-1, n + 1):
            cx = (col + 0.5) * d
            cy = (row + 0.5) * d
            for ox, oy in WRAPS:
                px, py = cx + ox, cy + oy
                if -15 <= px <= PERIOD + 15 and -15 <= py <= PERIOD + 15:
                    if (row + col) % 2 == 0:
                        skull(ax, px, py, s_skull, fill="black")
                    else:
                        draw_pentacle(ax, px, py, r_pent, lw=1.1, color="black")

    save(fig, "abstract halloween variation skull pentacle overlap dual motif interlocked grid pattern black white texture")


if __name__ == "__main__":
    draw()
