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
    """Wild: Cafe wall illusion (shifted rows of rectangles) using curved/arc rows instead of straight."""
    fig, ax = setup_ax()

    n_rows = 24
    n_tiles_per_row = 20
    tile_w = 5.0
    tile_h = 3.5

    for row in range(n_rows):
        # Each row is an arc — rows curve based on row index
        row_y_center = -42 + row * tile_h * 1.1
        row_shift = (tile_w / 2) * (row % 2)  # cafe-wall alternating shift
        curvature = 0.006 * (row - n_rows / 2)  # rows bow inward at center

        for col in range(-n_tiles_per_row // 2, n_tiles_per_row // 2 + 1):
            x_left = col * tile_w + row_shift
            x_right = x_left + tile_w

            # Curved row: y bows parabolicly
            x_center = (x_left + x_right) / 2
            y_base = row_y_center + curvature * x_center**2

            if (row + col) % 2 == 0:
                pts = np.array([
                    [x_left,  y_base],
                    [x_right, y_base],
                    [x_right, y_base + tile_h],
                    [x_left,  y_base + tile_h],
                ])
                from matplotlib.patches import Polygon
                poly = Polygon(pts, closed=True, facecolor="black", edgecolor="gray", linewidth=0.6)
                ax.add_patch(poly)

    save(fig, "abstract optical cafe wall illusion curved arc row pattern black white texture")


if __name__ == "__main__":
    generate()
