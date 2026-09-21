import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
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
    """Tweak: Ehrenstein starbursts sitting in rounded-block Hermann gaps, denser and shifted."""
    fig, ax = setup_ax()

    n = 9
    gap = 2.0
    block = (100.0 - gap) / n - gap
    step = block + gap
    rounding = 1.35

    for r in range(n):
        for c in range(n):
            x = gap * 0.55 + c * step
            y = gap * 0.55 + r * step
            ax.add_patch(
                FancyBboxPatch(
                    (x, y),
                    block,
                    block,
                    boxstyle=f"round,pad=0,rounding_size={rounding:.2f}",
                    facecolor="black",
                    edgecolor="none",
                    zorder=1,
                )
            )

    n_burst = 10
    burst_len = gap * 0.95
    for r in range(n + 1):
        for c in range(n + 1):
            ix = gap * 0.55 + c * step - gap * 0.5
            iy = gap * 0.55 + r * step - gap * 0.5
            for k in range(n_burst):
                a = k * np.pi / n_burst + 0.18 * (r + c)
                dx = burst_len * np.cos(a)
                dy = burst_len * np.sin(a)
                ax.plot([ix - dx, ix + dx], [iy - dy, iy + dy], color="black", linewidth=0.9, zorder=2)
            ax.add_patch(Circle((ix, iy), 0.28, facecolor="white", edgecolor="black", linewidth=0.3, zorder=3))

    save(
        fig,
        "abstract optical ehrenstein hermann rounded gap starburst dense pattern black white texture",
    )


if __name__ == "__main__":
    generate()
