import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
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
    """Wild: Cafe wall illusion meets vortex — tile rows are arranged in concentric rings with angular shift."""
    fig, ax = setup_ax()

    n_rings = 22
    n_tiles_per_ring = 30
    r_vals = np.linspace(5, 48, n_rings + 1)

    for i in range(n_rings):
        r1, r2 = r_vals[i], r_vals[i + 1]
        # Cafe-wall shift: alternating angular offset
        angle_shift = (np.pi / n_tiles_per_ring) * (i % 2)

        theta_vals = np.linspace(0, 2 * np.pi, n_tiles_per_ring + 1) + angle_shift

        for j in range(n_tiles_per_ring):
            if (i + j) % 2 == 0:
                t1, t2 = theta_vals[j], theta_vals[j + 1]
                t_seg = np.linspace(t1, t2, 12)
                outer = np.column_stack([r2 * np.cos(t_seg), r2 * np.sin(t_seg)])
                inner = np.column_stack([r1 * np.cos(t_seg[::-1]), r1 * np.sin(t_seg[::-1])])
                pts = np.vstack([outer, inner])
                poly = Polygon(pts, closed=True, facecolor="black",
                               edgecolor="black", linewidth=0.3)
                ax.add_patch(poly)

    # Thin ring mortar lines
    for r in r_vals:
        ax.add_patch(Circle((0, 0), r, fill=False, edgecolor="gray", linewidth=0.8))

    save(fig, "abstract optical cafe wall vortex polar ring shift pattern black white texture")


if __name__ == "__main__":
    generate()
