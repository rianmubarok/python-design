import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
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
    """Cafe wall with diamond/rhombus tiles instead of rectangles."""
    fig, ax = setup_ax()

    n_rows = 18
    n_cols = 16
    tile_w = 7.0
    tile_h = 5.5
    offsets = [0, 0.35, 0.5, 0.35, 0, -0.35, -0.5, -0.35]

    # Center the grid on canvas (50, 50)
    total_h = n_rows * tile_h
    total_w = n_cols * tile_w
    y_offset = (100 - total_h) / 2
    x_offset = (100 - total_w) / 2

    for r in range(n_rows):
        y_center = y_offset + r * tile_h + tile_h / 2
        shift = offsets[r % len(offsets)] * tile_w

        for c in range(-2, n_cols + 2):
            if (c + r) % 2 == 0:
                x_center = x_offset + c * tile_w + tile_w / 2 + shift
                # Diamond shape
                pts = np.array([
                    [x_center, y_center + tile_h / 2],
                    [x_center + tile_w / 2, y_center],
                    [x_center, y_center - tile_h / 2],
                    [x_center - tile_w / 2, y_center],
                ])
                poly = Polygon(pts, closed=True, facecolor="black", edgecolor="black", linewidth=0.3)
                ax.add_patch(poly)

        ax.plot([0, 100], [y_center - tile_h / 2, y_center - tile_h / 2],
                color="gray", linewidth=1.0)

    save(fig, "abstract optical cafe wall illusion diamond rhombus tile pattern black white texture")


if __name__ == "__main__":
    generate()
