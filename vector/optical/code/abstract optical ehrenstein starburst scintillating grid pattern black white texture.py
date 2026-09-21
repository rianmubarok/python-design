import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
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


def abstract_optical_ehrenstein_starburst_scintillating_grid_pattern_black_white_texture():
    """Optical experiment: Ehrenstein starburst grid producing scintillating illusory dots at intersections."""
    fig, ax = setup_ax()

    grid_n = 10
    coords = np.linspace(-42, 42, grid_n)
    sq_size = 6.2

    # Draw dark grid blocks
    for x in coords[:-1]:
        for y in coords[:-1]:
            cx = (x + coords[coords.tolist().index(x) + 1]) / 2
            cy = (y + coords[coords.tolist().index(y) + 1]) / 2

            rect = Rectangle(
                (cx - sq_size / 2, cy - sq_size / 2),
                sq_size,
                sq_size,
                facecolor="black",
                edgecolor="none",
            )
            ax.add_patch(rect)

    # Draw Ehrenstein radial starburst lines at grid intersections
    for x in coords:
        for y in coords:
            # Concentric circular ring boundary
            ring = plt.Circle(
                (x, y),
                1.4,
                fill=True,
                facecolor="white",
                edgecolor="black",
                linewidth=1.2,
            )
            ax.add_patch(ring)

            # Radial spokes terminating at ring
            n_rays = 12
            angles = np.linspace(0, 2 * np.pi, n_rays, endpoint=False)
            r_inner = 1.4
            r_outer = 2.8

            for a in angles:
                x1 = x + r_inner * np.cos(a)
                y1 = y + r_inner * np.sin(a)
                x2 = x + r_outer * np.cos(a)
                y2 = y + r_outer * np.sin(a)
                ax.plot([x1, x2], [y1, y2], color="black", linewidth=1.5)

    save(
        fig,
        "abstract optical ehrenstein starburst scintillating grid pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_ehrenstein_starburst_scintillating_grid_pattern_black_white_texture()
