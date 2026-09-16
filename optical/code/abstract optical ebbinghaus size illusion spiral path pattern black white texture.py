import numpy as np
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


def generate():
    """Ebbinghaus but arranged along a spiral path, with radius-based context size modulation."""
    fig, ax = setup_ax()

    n_clusters = 18
    spiral_turns = 2.5
    max_r = 42

    for k in range(n_clusters):
        t = k / n_clusters * spiral_turns * 2 * np.pi
        r = 8 + (max_r - 8) * (k / n_clusters)
        cx = r * np.cos(t)
        cy = r * np.sin(t)

        # Central dot (all identical size)
        center_r = 2.5
        ax.add_patch(Circle((cx, cy), center_r, facecolor="black"))

        # Surrounding context circles — size grows with spiral radius
        is_large = k % 2 == 0
        n_outer = 6 if is_large else 8
        outer_r = 3.5 + k * 0.2 if is_large else 1.0 + k * 0.05
        ring_r = center_r + outer_r + 1.5

        for j in range(n_outer):
            a = j * 2 * np.pi / n_outer
            ox = cx + ring_r * np.cos(a)
            oy = cy + ring_r * np.sin(a)
            ax.add_patch(Circle((ox, oy), outer_r, fill=False,
                                edgecolor="black", linewidth=1.5))

    save(fig, "abstract optical ebbinghaus size illusion spiral path pattern black white texture")


if __name__ == "__main__":
    generate()
