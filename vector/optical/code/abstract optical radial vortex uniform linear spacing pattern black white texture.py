import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
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
    """Wild: Vortex with linearly-spaced rings instead of geomspace — uniform band width throughout."""
    fig, ax = setup_ax()

    num_rings = 50
    num_sectors = 40
    r_boundaries = np.linspace(2.0, 48.0, num_rings)
    sector_angle = 360.0 / num_sectors

    for i in range(len(r_boundaries) - 1):
        r1 = r_boundaries[i]
        r2 = r_boundaries[i + 1]
        twist_offset = i * 2.0

        for j in range(num_sectors):
            theta1 = j * sector_angle + twist_offset
            theta2 = theta1 + sector_angle
            fill_color = "black" if (i + j) % 2 == 0 else "white"

            wedge = Wedge(
                (0, 0), r2, theta1, theta2,
                width=r2 - r1,
                facecolor=fill_color,
                edgecolor="black",
                linewidth=0.3,
            )
            ax.add_patch(wedge)

    save(fig, "abstract optical radial vortex uniform linear spacing pattern black white texture")


if __name__ == "__main__":
    generate()
