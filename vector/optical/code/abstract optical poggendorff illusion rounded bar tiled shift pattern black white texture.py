import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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


def generate():
    """Wild: Poggendorff diagonal interrupted by a thick rounded bar, tiled and shifted."""
    fig, ax = setup_ax()

    n = 4
    cell = 100.0 / n
    for r in range(n):
        for c in range(n):
            x0, y0 = c * cell, r * cell
            pad = 2.2
            # One continuous diagonal, interrupted by the occluder
            ax.plot(
                [x0 + pad, x0 + cell - pad],
                [y0 + pad, y0 + cell - pad],
                color="black",
                linewidth=2.3,
                zorder=1,
            )
            w = 4.2
            h = cell * 0.78
            xshift = 3.2 if (r + c) % 2 == 0 else -3.2
            ax.add_patch(
                FancyBboxPatch(
                    (x0 + cell / 2 - w / 2 + xshift, y0 + (cell - h) / 2),
                    w,
                    h,
                    boxstyle="round,pad=0,rounding_size=1.9",
                    facecolor="black",
                    edgecolor="none",
                    zorder=2,
                )
            )

    save(
        fig,
        "abstract optical poggendorff illusion rounded bar tiled shift pattern black white texture",
    )


if __name__ == "__main__":
    generate()
