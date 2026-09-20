import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
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
EPS_DIR = OUTPUT_DIR / \"eps\"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


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
    eps_path = EPS_DIR / f\"{name} {DATE}.eps\"
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format=\"eps\", pad_inches=0, facecolor=\"white\", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path} | {eps_path}")


def crossbones(ax, cx, cy, s, fill="black"):
    """Just the crossbones (no skull) — two bones crossed at 45°/135°."""
    bone_len = s * 1.10
    bone_w = s * 0.10
    knob_r = s * 0.085
    for ang in (45, -45):
        tr = Affine2D().rotate_deg(ang).translate(cx, cy) + ax.transData
        ax.add_patch(FancyBboxPatch(
            (-bone_len / 2, -bone_w / 2), bone_len, bone_w,
            boxstyle=f"round,pad=0,rounding_size={bone_w*0.45:.4f}",
            facecolor=fill, edgecolor="none", transform=tr))
        for end in (-bone_len / 2, bone_len / 2):
            ax.add_patch(Circle((end, 0), knob_r, facecolor=fill,
                                edgecolor="none", transform=tr))


def draw():
    """Crossbones-only pattern arranged on a rotated diamond (45°) lattice.
    The bones themselves are also at 45° so they align with the grid diagonals —
    creating a continuous bone-chain visual at tile intersections."""
    fig, ax = setup_ax()
    # Diamond lattice: offset every other column by half a row
    cols, rows = 9, 9
    step = PERIOD / cols
    s = step * 0.50
    for row in range(rows):
        for col in range(cols):
            # Rotated grid: diamond arrangement
            cx = (col + 0.5) * step + (step * 0.5 if row % 2 else 0)
            cy = (row + 0.5) * step
            fill = "black" if (row + col) % 2 == 0 else "white"
            edge_c = "white" if fill == "white" else "none"
            bg = "white" if fill == "black" else "black"
            for ox, oy in WRAPS:
                crossbones(ax, cx + ox, cy + oy, s, fill=fill)
    # overlay a faint diamond grid
    for row in range(rows + 1):
        for col in range(cols + 1):
            cx = col * step
            cy = row * step
    save(fig, "abstract halloween variation crossbones rotated diamond lattice pattern black white texture")


if __name__ == "__main__":
    draw()
