import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon
from matplotlib.transforms import Affine2D
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


def flame(ax, cx, cy, s, fill="black"):
    """Stylised candle flame — teardrop shape."""
    h = s * 0.38
    w = s * 0.16
    pts = []
    t = np.linspace(0, 2 * np.pi, 80)
    # parametric teardrop: r = cos(t/2)^2 style
    for a in t:
        r = w * (1 - 0.4 * np.sin(a)) * (0.6 + 0.4 * np.cos(a * 0.5))
        pts.append([cx + r * np.cos(a), cy + h * 0.5 + r * np.sin(a) * 0.9])
    # override with explicit simple teardrop
    n = 60
    pts = []
    for i in range(n):
        angle = np.pi * 2 * i / n
        # flame shape: wider at bottom, pointed at top
        rx = w * np.sin(angle)
        ry = h * (0.5 - 0.5 * np.cos(angle))
        pts.append([cx + rx, cy + ry])
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor="none"))
    # inner highlight
    ax.add_patch(Polygon(
        [(cx, cy + h * 0.65), (cx - w * 0.3, cy + h * 0.35), (cx + w * 0.3, cy + h * 0.35)],
        closed=True, facecolor="white" if fill == "black" else "black", edgecolor="none"))


def candle(ax, cx, cy, s, fill="black", inv="white"):
    """Candle stick with drip and flame on top."""
    cw = s * 0.22
    ch = s * 0.36
    # candle body
    ax.add_patch(FancyBboxPatch(
        (cx - cw / 2, cy - s * 0.50), cw, ch,
        boxstyle=f"round,pad=0,rounding_size={cw*0.15:.4f}",
        facecolor=fill, edgecolor="none"))
    # wax drip
    ax.add_patch(Ellipse((cx, cy - s * 0.50 + ch), cw * 1.2, cw * 0.28,
                         facecolor=fill, edgecolor="none"))
    # wick
    ax.plot([cx, cx], [cy - s * 0.50 + ch, cy - s * 0.50 + ch + s * 0.08],
            color=fill, linewidth=1.0)
    # flame
    flame(ax, cx, cy - s * 0.50 + ch + s * 0.08, s, fill=fill)


def skull_small(ax, cx, cy, s, fill="black", inv="white"):
    """Compact skull above candle."""
    for ang in (35, -35):
        tr = Affine2D().rotate_deg(ang).translate(cx, cy - 0.42 * s) + ax.transData
        ax.add_patch(FancyBboxPatch(
            (-0.62 * s, -0.055 * s), 1.24 * s, 0.11 * s,
            boxstyle=f"round,pad=0,rounding_size={0.05*s:.4f}",
            facecolor=fill, edgecolor="none", transform=tr))
        for end in (-0.6 * s, 0.6 * s):
            ax.add_patch(Circle((end, 0), 0.085 * s, facecolor=fill,
                                edgecolor="none", transform=tr))
    ax.add_patch(Ellipse((cx, cy + 0.16 * s), 0.82 * s, 0.74 * s, facecolor=fill, edgecolor="none"))
    ax.add_patch(FancyBboxPatch(
        (cx - 0.26 * s, cy - 0.24 * s), 0.52 * s, 0.26 * s,
        boxstyle=f"round,pad=0,rounding_size={0.04*s:.4f}",
        facecolor=fill, edgecolor="none"))
    for sx in (-0.17 * s, 0.17 * s):
        ax.add_patch(Ellipse((cx + sx, cy + 0.185 * s), 0.22 * s, 0.25 * s,
                             facecolor=inv, edgecolor="none"))
    ax.add_patch(Polygon(
        [[cx, cy + 0.035 * s], [cx - 0.07 * s, cy - 0.07 * s], [cx + 0.07 * s, cy - 0.07 * s]],
        closed=True, facecolor=inv, edgecolor="none"))
    for x in (-0.13 * s, 0.0, 0.13 * s):
        ax.add_patch(FancyBboxPatch(
            (cx + x - 0.028 * s, cy - 0.205 * s), 0.056 * s, 0.115 * s,
            facecolor=inv, edgecolor="none"))


def draw():
    """Each tile = small skull sitting atop a candle — 5×6 alternating fill grid."""
    fig, ax = setup_ax()
    cols, rows = 5, 6
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.36   # skull size
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            fill = "black" if (row + col) % 2 == 0 else "white"
            inv = "white" if fill == "black" else "black"
            bg = inv
            # background cell
            ax.add_patch(FancyBboxPatch(
                (cx - dx / 2, cy - dy / 2), dx, dy,
                boxstyle="square,pad=0",
                facecolor=bg, edgecolor="none"))
            for ox, oy in WRAPS:
                # candle placed just below skull
                candle(ax, cx + ox, cy + oy - s * 0.4, s * 0.85, fill=fill, inv=inv)
                skull_small(ax, cx + ox, cy + oy + s * 0.5, s, fill=fill, inv=inv)
    save(fig, "abstract halloween variation skull candle flame combo repeating pattern black white texture")


if __name__ == "__main__":
    draw()
