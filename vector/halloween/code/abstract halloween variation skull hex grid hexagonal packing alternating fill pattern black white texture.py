import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon
from matplotlib.transforms import Affine2D
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


def skull(ax, cx, cy, s, fill="black"):
    """Skull-and-crossbones silhouette.
    Black fill  → solid black, no edge.
    White fill  → white body with bold black outline on every shape piece,
                  giving a clean readable white-on-white-bg look.
    """
    inv  = "white" if fill == "black" else "black"
    edge = "none"  if fill == "black" else "black"
    elw  = 0.0     if fill == "black" else s * 0.10   # thick outline for white variant

    # ── CROSSBONES ──────────────────────────────────────────────────────────
    # Centred ~0.38s below skull centre
    bone_cy = cy - 0.36 * s

    for ang in (42, -42):
        tr = Affine2D().rotate_deg(ang).translate(cx, bone_cy) + ax.transData
        ax.add_patch(FancyBboxPatch(
            (-0.50 * s, -0.044 * s), 1.00 * s, 0.088 * s,
            boxstyle=f"round,pad=0,rounding_size={0.038*s:.4f}",
            facecolor=fill, edgecolor=edge, linewidth=elw,
            transform=tr))
        for end_x in (-0.48 * s, 0.48 * s):
            ax.add_patch(Circle(
                (end_x, 0), 0.068 * s,
                facecolor=fill, edgecolor=edge, linewidth=elw,
                transform=tr))

    # ── SKULL ────────────────────────────────────────────────────────────────
    skull_cy = cy + 0.10 * s   # skull body sits above bone centre

    # cranium (slightly wider than tall)
    ax.add_patch(Ellipse(
        (cx, skull_cy + 0.09 * s), 0.72 * s, 0.64 * s,
        facecolor=fill, edgecolor=edge, linewidth=elw))

    # jaw (rounded rect below cranium)
    ax.add_patch(FancyBboxPatch(
        (cx - 0.22 * s, skull_cy - 0.20 * s), 0.44 * s, 0.19 * s,
        boxstyle=f"round,pad=0,rounding_size={0.038*s:.4f}",
        facecolor=fill, edgecolor=edge, linewidth=elw))

    # ── FACE FEATURES ────────────────────────────────────────────────────────
    eye_y = skull_cy + 0.13 * s

    # eye sockets
    for ex in (-0.155 * s, 0.155 * s):
        ax.add_patch(Ellipse(
            (cx + ex, eye_y), 0.16 * s, 0.18 * s,
            facecolor=inv, edgecolor="none"))

    # nose cavity (triangle)
    ax.add_patch(Polygon(
        np.array([[cx,            skull_cy + 0.00 * s],
                  [cx - 0.055*s, skull_cy - 0.075 * s],
                  [cx + 0.055*s, skull_cy - 0.075 * s]]),
        closed=True, facecolor=inv, edgecolor="none"))

    # teeth (3)
    for tx in (-0.095 * s, 0.0, 0.095 * s):
        ax.add_patch(FancyBboxPatch(
            (cx + tx - 0.022 * s, skull_cy - 0.180 * s),
            0.044 * s, 0.088 * s,
            boxstyle="round,pad=0,rounding_size=0.004",
            facecolor=inv, edgecolor="none"))


def draw():
    """True hexagonal close-pack skull grid.

    Geometry:
      hex_w  = horizontal distance between adjacent skull centres in same row
      hex_h  = hex_w * sqrt(3)/2  — vertical distance between rows
      Odd rows are shifted right by hex_w/2 (standard pointy-top hex packing).

    Skull scale s = hex_w * 0.46 — fills ~92% of the hex cell diameter so
    skulls sit snug without overlapping.

    Alternating fill: black when (row+col) % 2 == 0, white otherwise.
    White skulls carry a thick black edge so they read clearly on white bg.
    """
    fig, ax = setup_ax()

    cols  = 7
    hex_w = PERIOD / cols                  # ~14.3 units between centres
    hex_h = hex_w * (np.sqrt(3) / 2)      # ~12.4 units — true hex row spacing
    rows  = int(np.ceil(PERIOD / hex_h)) + 2
    s     = hex_w * 0.46                  # skull fits snugly in hex cell

    for row in range(-1, rows + 1):
        offset = (hex_w * 0.5) if (row % 2 != 0) else 0.0
        for col in range(-1, cols + 2):
            cx   = col * hex_w + offset + hex_w * 0.5
            cy   = row * hex_h + hex_h * 0.5      # centred within row band
            fill = "black" if (row + col) % 2 == 0 else "white"
            for ox, oy in WRAPS:
                skull(ax, cx + ox, cy + oy, s, fill=fill)

    save(fig,
         "abstract halloween variation skull hex grid hexagonal packing "
         "alternating fill pattern black white texture")


if __name__ == "__main__":
    draw()
