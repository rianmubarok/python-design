import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
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


def draw():
    """
    Dual Source Ripple Interference.
    Two sets of concentric circles overlapping, like two raindrops 
    hitting a pond simultaneously, creating a moire interference pattern.
    """
    fig, ax = setup_ax()

    centers = [(35.0, 50.0), (65.0, 50.0)]
    n_circles = 50
    max_radius = 80.0
    
    # We will draw them using very fine points so we don't have overlapping line issues,
    # but since it's matplotlib, overlapping thin lines naturally create the moire effect.

    for cx, cy in centers:
        for i in range(1, n_circles + 1):
            r = max_radius * (i / n_circles)
            circle = plt.Circle((cx, cy), r, color="black", fill=False, linewidth=1.0)
            ax.add_patch(circle)

    save(fig, "abstract concentric circles ripple interference dual source pattern black white texture")


if __name__ == "__main__":
    draw()
