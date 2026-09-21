import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.transforms import Affine2D
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
    """Tweak: Radial vortex stretched into an anamorphic ellipse (not a seamless tile)."""
    fig, ax = setup_ax()

    sx, sy = 1.38, 0.70
    num_rings = 42
    num_sectors = 36
    r_bounds = np.linspace(1.6, 58.0, num_rings)
    sector = 360.0 / num_sectors
    stretch = Affine2D().scale(sx, sy) + ax.transData

    for i in range(len(r_bounds) - 1):
        r0, r1 = r_bounds[i], r_bounds[i + 1]
        for s in range(num_sectors):
            if (i + s) % 2:
                continue
            theta0 = s * sector + i * 2.4
            theta1 = theta0 + sector
            wedge = Wedge(
                (0, 0),
                r1,
                theta0,
                theta1,
                width=r1 - r0,
                facecolor="black",
                edgecolor="none",
            )
            wedge.set_transform(stretch)
            ax.add_patch(wedge)

    save(
        fig,
        "abstract optical radial vortex elliptic stretch anamorphic pattern black white texture",
    )


if __name__ == "__main__":
    generate()
