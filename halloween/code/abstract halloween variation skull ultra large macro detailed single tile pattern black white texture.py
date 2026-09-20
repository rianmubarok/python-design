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


def draw_skull_large(ax, cx, cy, s):
    """Ultra-large skull with extra tooth/jaw detail, cracks, and shading lines."""
    fill, inv = "black", "white"

    # ==== CROSSBONES ====
    for ang in (38, -38):
        tr = Affine2D().rotate_deg(ang).translate(cx, cy - 0.44 * s) + ax.transData
        ax.add_patch(FancyBboxPatch(
            (-0.65 * s, -0.06 * s), 1.30 * s, 0.12 * s,
            boxstyle=f"round,pad=0,rounding_size={0.055*s:.4f}",
            facecolor=fill, edgecolor="none", transform=tr))
        for end in (-0.62 * s, 0.62 * s):
            ax.add_patch(Circle((end, 0), 0.095 * s, facecolor=fill,
                                edgecolor="none", transform=tr))

    # ==== CRANIUM ====
    ax.add_patch(Ellipse((cx, cy + 0.18 * s), 0.88 * s, 0.80 * s,
                         facecolor=fill, edgecolor="none"))

    # ==== JAW ====
    ax.add_patch(FancyBboxPatch(
        (cx - 0.28 * s, cy - 0.26 * s), 0.56 * s, 0.30 * s,
        boxstyle=f"round,pad=0,rounding_size={0.06*s:.4f}",
        facecolor=fill, edgecolor="none"))

    # ==== EYE SOCKETS ====
    for sx in (-0.20 * s, 0.20 * s):
        # outer socket
        ax.add_patch(Ellipse((cx + sx, cy + 0.22 * s), 0.26 * s, 0.28 * s,
                             facecolor=inv, edgecolor="none"))
        # inner shadow ring
        ax.add_patch(Ellipse((cx + sx + 0.02 * s, cy + 0.20 * s), 0.16 * s, 0.18 * s,
                             facecolor=fill, edgecolor="none"))

    # ==== NOSE CAVITY ====
    nose = np.array([
        [cx,           cy + 0.05 * s],
        [cx - 0.09 * s, cy - 0.09 * s],
        [cx - 0.04 * s, cy - 0.13 * s],
        [cx + 0.04 * s, cy - 0.13 * s],
        [cx + 0.09 * s, cy - 0.09 * s],
    ])
    ax.add_patch(Polygon(nose, closed=True, facecolor=inv, edgecolor="none"))

    # ==== TEETH — 6 detailed teeth ====
    tooth_xs = np.linspace(cx - 0.22 * s, cx + 0.22 * s, 6)
    for tx in tooth_xs:
        ax.add_patch(FancyBboxPatch(
            (tx - 0.028 * s, cy - 0.24 * s), 0.050 * s, 0.14 * s,
            boxstyle=f"round,pad=0,rounding_size={0.012*s:.4f}",
            facecolor=inv, edgecolor="none"))
        # lower jaw tooth
        ax.add_patch(FancyBboxPatch(
            (tx - 0.026 * s, cy - 0.46 * s), 0.046 * s, 0.12 * s,
            boxstyle=f"round,pad=0,rounding_size={0.010*s:.4f}",
            facecolor=inv, edgecolor="none"))

    # gum line divider
    ax.plot([cx - 0.28 * s, cx + 0.28 * s], [cy - 0.26 * s, cy - 0.26 * s],
            color=inv, linewidth=0.8)

    # ==== CRACKS on cranium ====
    crack_segs = [
        [(cx + 0.10 * s, cy + 0.42 * s), (cx + 0.18 * s, cy + 0.30 * s),
         (cx + 0.22 * s, cy + 0.20 * s)],
        [(cx - 0.05 * s, cy + 0.38 * s), (cx - 0.14 * s, cy + 0.28 * s),
         (cx - 0.10 * s, cy + 0.18 * s)],
    ]
    for seg in crack_segs:
        xs = [p[0] for p in seg]
        ys = [p[1] for p in seg]
        ax.plot(xs, ys, color=inv, linewidth=0.7, solid_capstyle="round",
                solid_joinstyle="round")

    # ==== CHEEKBONE shading lines ====
    for sx, sign in ((-1, -1), (1, 1)):
        for i in range(4):
            offset = i * s * 0.04
            ax.plot([cx + sign * (0.35 * s + offset),
                     cx + sign * (0.42 * s + offset * 0.5)],
                    [cy + 0.08 * s - i * s * 0.05,
                     cy + 0.12 * s - i * s * 0.04],
                    color=inv, linewidth=0.45, alpha=0.8)


def draw():
    """3×3 large skull grid — each skull nearly fills the tile, maximum detail."""
    fig, ax = setup_ax()
    cols, rows = 3, 3
    dx, dy = PERIOD / cols, PERIOD / rows
    s = min(dx, dy) * 0.86
    for row in range(rows):
        for col in range(cols):
            cx = (col + 0.5) * dx
            cy = (row + 0.5) * dy
            for ox, oy in WRAPS:
                draw_skull_large(ax, cx + ox, cy + oy, s)
    save(fig, "abstract halloween variation skull ultra large macro detailed single tile pattern black white texture")


if __name__ == "__main__":
    draw()
