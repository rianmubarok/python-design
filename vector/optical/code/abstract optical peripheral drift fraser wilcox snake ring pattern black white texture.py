import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
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


def snake_ring(ax, cx, cy, r_in, r_out, n_seg, phase, flip):
    step = 360.0 / n_seg
    for i in range(n_seg):
        a0 = i * step + phase
        a1 = a0 + step
        parity = (i + flip) % 4
        if parity == 0:
            color = "black"
        elif parity == 1:
            color = "#b8b8b8"
        elif parity == 2:
            color = "white"
        else:
            color = "#4a4a4a"
        ax.add_patch(
            Wedge(
                (cx, cy),
                r_out,
                a0,
                a1,
                width=r_out - r_in,
                facecolor=color,
                edgecolor="black",
                linewidth=0.25,
            )
        )


def generate():
    """Wild: Fraser–Wilcox / peripheral-drift snake rings in a seamless hexagonal lattice."""
    fig, ax = setup_ax()
    ax.add_patch(plt.Rectangle((0, 0), 100, 100, facecolor="#ececec", edgecolor="none"))

    cols, rows = 6, 7
    dx = 100.0 / cols
    dy = dx * np.sqrt(3) / 2
    y0 = (100 - dy * (rows - 1)) / 2
    r_out = dx * 0.42

    for r in range(rows):
        x_off = dx * 0.5 if r % 2 else 0.0
        for c in range(cols):
            cx = (c + 0.5) * dx + x_off
            cy = y0 + r * dy
            if cx < -8 or cx > 108:
                continue
            flip = (r + c) % 2
            snake_ring(ax, cx, cy, r_out * 0.22, r_out, 16, 12 * (r + c), flip)
            ax.add_patch(Circle((cx, cy), r_out * 0.16, facecolor="black", edgecolor="none"))

    save(
        fig,
        "abstract optical peripheral drift fraser wilcox snake ring pattern black white texture",
    )


if __name__ == "__main__":
    generate()
