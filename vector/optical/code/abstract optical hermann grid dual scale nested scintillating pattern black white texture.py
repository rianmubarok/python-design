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


def hermann(ax, origin, size, n, gap_ratio, rounding_ratio, z):
    gap = size * gap_ratio
    block = (size - gap) / n - gap
    step = block + gap
    for r in range(n):
        for c in range(n):
            x = origin[0] + gap * 0.5 + c * step
            y = origin[1] + gap * 0.5 + r * step
            ax.add_patch(
                FancyBboxPatch(
                    (x, y),
                    block,
                    block,
                    boxstyle=f"round,pad=0,rounding_size={block * rounding_ratio:.3f}",
                    facecolor="black",
                    edgecolor="none",
                    zorder=z,
                )
            )


def generate():
    """Tweak: Dual-scale nested Hermann grids — coarse blocks contain a finer scintillating grid."""
    fig, ax = setup_ax()
    n_macro = 4
    cell = 100.0 / n_macro
    for r in range(n_macro):
        for c in range(n_macro):
            ox, oy = c * cell, r * cell
            hermann(ax, (ox + 2.2, oy + 2.2), cell - 4.4, 5, 0.12, 0.18, 1)

    save(
        fig,
        "abstract optical hermann grid dual scale nested scintillating pattern black white texture",
    )


if __name__ == "__main__":
    generate()
