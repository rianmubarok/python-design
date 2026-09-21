import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path
from datetime import datetime
from matplotlib.transforms import Affine2D

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
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
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


def draw_rings(ax, cx, cy, angle, n, max_s, rounding_ratio, lw):
    trans = Affine2D().rotate_deg(angle).translate(cx, cy) + ax.transData
    for i in range(n):
        s = max_s * (1 - i / n)
        if s < 1.2:
            break
        rounding = min(s * rounding_ratio, s * 0.48)
        patch = FancyBboxPatch(
            (-s, -s),
            2 * s,
            2 * s,
            boxstyle=f"round,pad=0,rounding_size={rounding:.2f}",
            facecolor="none",
            edgecolor="black",
            linewidth=lw,
        )
        patch.set_transform(trans)
        ax.add_patch(patch)


def generate():
    """Tweak: Concentric rounded-square ring moiré with dual offset centers."""
    fig, ax = setup_ax()
    draw_rings(ax, -2.2, -1.8, 0, 55, 58, 0.18, 0.85)
    draw_rings(ax, 2.4, 2.0, 3.2, 55, 58, 0.28, 0.75)
    save(
        fig,
        "abstract optical moire concentric rounded square ring offset pattern black white texture",
    )


if __name__ == "__main__":
    generate()
