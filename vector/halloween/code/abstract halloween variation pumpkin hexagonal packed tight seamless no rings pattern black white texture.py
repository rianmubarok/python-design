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


def draw_pumpkin(ax, cx, cy, s, fill="white"):
    """Compact jack-o'-lantern silhouette with face, no aura rings."""
    inv = "black" if fill == "white" else "white"

    # Three lobes
    for lobe_ox in (-s * 0.22, 0, s * 0.22):
        ax.add_patch(Ellipse((cx + lobe_ox, cy), s * 0.56, s * 0.74,
                             facecolor=fill, edgecolor="none"))
    # Stem
    ax.add_patch(FancyBboxPatch(
        (cx - s * 0.055, cy + s * 0.35), s * 0.11, s * 0.15,
        boxstyle=f"round,pad=0,rounding_size={s*0.025:.4f}",
        facecolor=fill, edgecolor="none"))

    # Triangle eyes
    for sign in (-1, 1):
        eye = np.array([
            [cx + sign * s * 0.24, cy + s * 0.14],
            [cx + sign * s * 0.34, cy - s * 0.02],
            [cx + sign * s * 0.14, cy - s * 0.02],
        ])
        ax.add_patch(Polygon(eye, closed=True, facecolor=inv, edgecolor="none"))

    # Jagged mouth
    teeth_x = np.linspace(cx - s * 0.26, cx + s * 0.26, 7)
    mouth_pts = [(teeth_x[0], cy - s * 0.11)]
    for k, x in enumerate(teeth_x):
        mouth_pts.append((x, cy - s * 0.24 if k % 2 == 0 else cy - s * 0.11))
    mouth_pts.append((teeth_x[-1], cy - s * 0.11))
    ax.add_patch(Polygon(mouth_pts, closed=True, facecolor=inv, edgecolor="none"))


def draw():
    """True hexagonal close-pack of pumpkins — 8 columns.
    Alternating black/white fill per (row+col) parity.
    No aura rings — pure packed silhouettes, black background.
    """
    fig, ax = setup_ax()

    cols  = 8
    hex_w = PERIOD / cols
    hex_h = hex_w * (np.sqrt(3) / 2)
    rows  = int(np.ceil(PERIOD / hex_h)) + 2
    s     = hex_w * 0.44

    for row in range(-1, rows + 1):
        offset = (hex_w * 0.5) if (row % 2 != 0) else 0.0
        for col in range(-1, cols + 2):
            cx   = col * hex_w + offset + hex_w * 0.5
            cy   = row * hex_h + hex_h * 0.5
            fill = "white" if (row + col) % 2 == 0 else "black"
            for ox, oy in WRAPS:
                draw_pumpkin(ax, cx + ox, cy + oy, s, fill=fill)

    save(fig,
         "abstract halloween variation pumpkin hexagonal packed tight seamless "
         "no rings pattern black white texture")


if __name__ == "__main__":
    draw()
