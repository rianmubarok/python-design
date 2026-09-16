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
    """Wild: Poggendorff on diagonal — lines pass behind diagonal bands at 45 degrees."""
    fig, ax = setup_ax()

    # Draw diagonal occluding bands at 45 degrees
    band_width = 8.0
    n_bands = 8
    for k in range(n_bands):
        offset = -80 + k * 22
        x = np.array([offset, offset + band_width, offset + band_width + 100, offset + 100])
        y = np.array([-50, -50, 50, 50])
        from matplotlib.patches import Polygon
        pts = np.column_stack([
            [offset, offset + band_width, offset + band_width + 100, offset + 100],
            [-50, -50, 50, 50]
        ])
        # Draw as fill_between approximation
        ax.fill_betweenx([-50, 50],
                         [offset - 50, offset + 50],
                         [offset + band_width - 50, offset + band_width + 50],
                         color="black", alpha=0.15)

    # Draw the "interrupted" lines that create misalignment illusion
    n_lines = 20
    for i in range(n_lines):
        y_start = -48 + i * 5
        # Line segments visible between bands
        for k in range(n_bands + 1):
            x_start = -50 + k * 22 + band_width
            x_end = -50 + (k + 1) * 22
            if x_start < 50 and x_end > -50:
                x_start = max(x_start, -50)
                x_end = min(x_end, 50)
                # Slight vertical offset to create Poggendorff misalignment
                y_shift = 0.8 * (k % 2 * 2 - 1)
                ax.plot([x_start, x_end],
                        [y_start + y_shift, y_start + y_shift],
                        color="black", linewidth=1.8)

    save(fig, "abstract optical poggendorff illusion diagonal band shift pattern black white texture")


if __name__ == "__main__":
    generate()
