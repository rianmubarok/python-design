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
    print(f"Saved: {jpg_path} | {svg_path}")


def skull(ax, cx, cy, s, fill="black", depth=0):
    """Skull with optional recursive tiny skulls drawn inside each eye socket."""
    inv = "white" if fill == "black" else "black"
    edge = "none"

    # crossbones (only on top-level skull)
    if depth == 0:
        for ang in (38, -38):
            tr = Affine2D().rotate_deg(ang).translate(cx, cy - 0.42 * s) + ax.transData
            ax.add_patch(FancyBboxPatch(
                (-0.58 * s, -0.05 * s), 1.16 * s, 0.10 * s,
                boxstyle=f"round,pad=0,rounding_size={0.046*s:.4f}",
                facecolor=fill, edgecolor=edge, transform=tr))
            for end in (-0.57 * s, 0.57 * s):
                ax.add_patch(Circle((end, 0), 0.08 * s, facecolor=fill,
                                    edgecolor=edge, transform=tr))

    # cranium
    ax.add_patch(Ellipse((cx, cy + 0.14 * s), 0.80 * s, 0.72 * s,
                         facecolor=fill, edgecolor=edge))
    # jaw
    ax.add_patch(FancyBboxPatch(
        (cx - 0.26 * s, cy - 0.22 * s), 0.52 * s, 0.23 * s,
        boxstyle=f"round,pad=0,rounding_size={0.04*s:.4f}",
        facecolor=fill, edgecolor=edge))

    # eye socket positions
    eye_positions = [(-0.18 * s, cy + 0.19 * s), (0.18 * s, cy + 0.19 * s)]
    eye_rx, eye_ry = 0.145 * s, 0.165 * s

    for (ex_off, ey) in eye_positions:
        ex = cx + ex_off
        if depth < 2:
            # draw a tiny skull inside the eye socket
            micro_s = s * 0.19
            skull(ax, ex, ey, micro_s, fill=inv, depth=depth + 1)
            # outline the socket to frame the micro skull
            ax.add_patch(Ellipse((ex, ey), eye_rx * 2, eye_ry * 2,
                                 facecolor="none", edgecolor=inv, linewidth=0.4))
        else:
            ax.add_patch(Ellipse((ex, ey), eye_rx * 2, eye_ry * 2,
                                 facecolor=inv, edgecolor=edge))

    # nose
    ax.add_patch(Polygon(
        np.array([[cx, cy + 0.02 * s],
                  [cx - 0.065 * s, cy - 0.075 * s],
                  [cx + 0.065 * s, cy - 0.075 * s]]),
        closed=True, facecolor=inv, edgecolor=edge))
    # teeth
    for tx in (-0.12 * s, 0.0, 0.12 * s):
        ax.add_patch(FancyBboxPatch(
            (cx + tx - 0.026 * s, cy - 0.19 * s), 0.052 * s, 0.105 * s,
            boxstyle="round,pad=0,rounding_size=0.005",
            facecolor=inv, edgecolor=edge))


def draw():
    """4×4 staggered skull grid. Each large skull has micro skulls inside its
    eye sockets, which in turn have even smaller skulls — 3 levels of recursion."""
    fig, ax = setup_ax()
    cols, rows = 4, 4
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.78

    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx + (dx * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                skull(ax, cx + ox, cy + oy, s, fill="black", depth=0)

    save(fig, "abstract halloween variation skull infinite regression tiny skulls eye sockets pattern black white texture")


if __name__ == "__main__":
    draw()
