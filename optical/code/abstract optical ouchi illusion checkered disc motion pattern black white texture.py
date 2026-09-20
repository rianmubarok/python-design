import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, PathPatch
from matplotlib.path import Path as MplPath
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def ellipse_path(cx, cy, w, h, n=80):
    t = np.linspace(0, 2 * np.pi, n)
    verts = np.column_stack([cx + (w / 2) * np.cos(t), cy + (h / 2) * np.sin(t)])
    codes = np.full(n, MplPath.LINETO)
    codes[0] = MplPath.MOVETO
    return MplPath(verts, codes)


def generate():
    """Wild: Ouchi motion illusion — checkered oval discs in a checker surround, seamless grid."""
    fig, ax = setup_ax()

    n = 10
    cell = 100.0 / n
    for r in range(n):
        for c in range(n):
            if (r + c) % 2 == 0:
                ax.add_patch(Rectangle((c * cell, r * cell), cell, cell, facecolor="black", edgecolor="none"))

    for r in range(n):
        for c in range(n):
            cx = (c + 0.5) * cell
            cy = (r + 0.5) * cell
            ew, eh = cell * 0.82, cell * 0.54
            clip = PathPatch(ellipse_path(cx, cy, ew, eh), transform=ax.transData, visible=False)
            ax.add_patch(clip)
            inner_n = 8
            iw, ih = ew / inner_n, eh / inner_n
            invert = (r + c) % 2 == 0
            for iy in range(inner_n):
                for ix in range(inner_n):
                    filled = (ix + iy) % 2 == 0
                    if invert:
                        color = "white" if filled else "black"
                    else:
                        color = "black" if filled else "white"
                    rect = Rectangle(
                        (cx - ew / 2 + ix * iw, cy - eh / 2 + iy * ih),
                        iw,
                        ih,
                        facecolor=color,
                        edgecolor="none",
                    )
                    rect.set_clip_path(clip)
                    ax.add_patch(rect)

    save(
        fig,
        "abstract optical ouchi illusion checkered disc motion pattern black white texture",
    )


if __name__ == "__main__":
    generate()
