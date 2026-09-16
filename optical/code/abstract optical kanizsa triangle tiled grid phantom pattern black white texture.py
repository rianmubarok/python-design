import numpy as np
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
    """Wild: Kanizsa triangle illusion tiled across a grid — pac-man inducers create phantom triangles everywhere."""
    fig, ax = setup_ax()
    from matplotlib.patches import Wedge

    spacing = 16.0
    pac_r = 4.0
    rows = 6
    cols = 6

    for r in range(rows):
        for c in range(cols):
            cx = (c - cols / 2 + 0.5) * spacing
            cy = (r - rows / 2 + 0.5) * spacing

            # Alternate between upward and downward pointing triangles
            if (r + c) % 2 == 0:
                # Three pac-men creating upward triangle
                positions = [
                    (cx - 5, cy - 3, 30),
                    (cx + 5, cy - 3, 150),
                    (cx, cy + 6, 270),
                ]
            else:
                # Three pac-men creating downward triangle
                positions = [
                    (cx - 5, cy + 3, 330),
                    (cx + 5, cy + 3, 210),
                    (cx, cy - 6, 90),
                ]

            for px, py, mouth_angle in positions:
                wedge = Wedge((px, py), pac_r, mouth_angle + 30, mouth_angle + 330,
                              facecolor="black", edgecolor="black")
                ax.add_patch(wedge)

    save(fig, "abstract optical kanizsa triangle tiled grid phantom pattern black white texture")


if __name__ == "__main__":
    generate()
