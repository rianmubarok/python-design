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
    Concentric regular pentagons.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_shapes = 35
    max_radius = 65.0

    for i in range(1, n_shapes + 1):
        r = max_radius * (i / n_shapes)
        
        # Vertices of a regular pentagon pointing upwards
        angles = np.array([np.pi/2 + 2*np.pi*k/5 for k in range(6)])
        x = cx + r * np.cos(angles)
        y = cy + r * np.sin(angles)
        
        ax.plot(x, y, color="black", linewidth=1.5, solid_capstyle="round", solid_joinstyle="round")

    save(fig, "abstract concentric polygons pentagon pattern black white texture")


if __name__ == "__main__":
    draw()
