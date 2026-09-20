import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
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
    """Tweak: Café wall with dense stadium (high corner-radius) tiles and larger row stagger."""
    fig, ax = setup_ax()

    n_rows = 18
    n_cols = 16
    row_h = 100.0 / n_rows
    col_w = 100.0 / n_cols
    mortar = 0.55
    offsets = [0.0, 0.35, 0.7, 0.35]
    rounding = min(row_h * 0.48, col_w * 0.42)

    ax.add_patch(Rectangle((0, 0), 100, 100, facecolor="white", edgecolor="none", zorder=0))

    for r in range(n_rows):
        y = r * row_h + mortar * 0.5
        h = row_h - mortar
        shift = offsets[r % len(offsets)] * col_w
        for c in range(-2, n_cols + 3):
            if (c + r) % 2 != 0:
                continue
            x = c * col_w + shift + mortar * 0.35
            w = col_w - mortar * 0.7
            ax.add_patch(
                FancyBboxPatch(
                    (x, y),
                    w,
                    h,
                    boxstyle=f"round,pad=0,rounding_size={rounding:.3f}",
                    facecolor="black",
                    edgecolor="none",
                    zorder=1,
                )
            )
        ax.plot([-5, 105], [r * row_h, r * row_h], color="#7a7a7a", linewidth=1.6, zorder=2)
    ax.plot([-5, 105], [100, 100], color="#7a7a7a", linewidth=1.6, zorder=2)

    save(
        fig,
        "abstract optical cafe wall illusion rounded stadium tile dense pattern black white texture",
    )


if __name__ == "__main__":
    generate()
