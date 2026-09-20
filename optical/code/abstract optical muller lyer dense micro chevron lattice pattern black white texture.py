import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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


def chevron(ax, x, y, inward, size):
    sign = 1.0 if inward else -1.0
    ax.plot([x, x + sign * size], [y, y + size * 0.72], color="black", linewidth=1.15)
    ax.plot([x, x + sign * size], [y, y - size * 0.72], color="black", linewidth=1.15)


def generate():
    """Tweak: Dense micro Müller-Lyer lattice, alternating inward/outward fins, seamless grid."""
    fig, ax = setup_ax()
    n_rows, n_cols = 14, 8
    ys = np.linspace(4, 96, n_rows)
    xs = np.linspace(8, 92, n_cols)
    half = 4.2
    fin = 1.55

    for i, y in enumerate(ys):
        for j, xc in enumerate(xs):
            x1, x2 = xc - half, xc + half
            ax.plot([x1, x2], [y, y], color="black", linewidth=1.35)
            inward = (i + j) % 2 == 0
            chevron(ax, x1, y, inward, fin)
            chevron(ax, x2, y, not inward, fin)

    save(
        fig,
        "abstract optical muller lyer dense micro chevron lattice pattern black white texture",
    )


if __name__ == "__main__":
    generate()
