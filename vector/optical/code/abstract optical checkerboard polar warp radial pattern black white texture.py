import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
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
    """Wild: Checkerboard that undergoes a POLAR warp — Cartesian grid remapped to polar coordinates."""
    fig, ax = setup_ax()

    n_rings = 40
    n_sectors = 50
    r_vals = np.linspace(0.05, 1.15, n_rings + 1)
    theta_vals = np.linspace(0, 2 * np.pi, n_sectors + 1)

    for i in range(n_rings):
        for j in range(n_sectors):
            if (i + j) % 2 == 0:
                r1, r2 = r_vals[i], r_vals[i + 1]
                t1, t2 = theta_vals[j], theta_vals[j + 1]

                t_seg = np.linspace(t1, t2, 10)
                outer = np.column_stack([r2 * np.cos(t_seg), r2 * np.sin(t_seg)])
                inner = np.column_stack([r1 * np.cos(t_seg[::-1]), r1 * np.sin(t_seg[::-1])])
                pts = np.vstack([outer, inner])

                poly = Polygon(pts, closed=True, facecolor="black",
                               edgecolor="black", linewidth=0.2)
                ax.add_patch(poly)

    save(fig, "abstract optical checkerboard polar warp radial pattern black white texture")


if __name__ == "__main__":
    generate()
