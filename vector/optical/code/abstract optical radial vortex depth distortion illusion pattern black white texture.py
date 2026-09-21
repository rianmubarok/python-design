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


def abstract_optical_radial_vortex_depth_distortion_illusion_pattern_black_white_texture():
    """Optical experiment: Radial ray vortex modulated by logarithmic spiral depth bands."""
    fig, ax = setup_ax()

    num_rings = 32
    num_sectors = 48

    # Exponential radial spacing for logarithmic depth perception
    r_boundaries = np.geomspace(2.0, 48.0, num_rings)
    sector_angle = 360.0 / num_sectors

    for i in range(len(r_boundaries) - 1):
        r1 = r_boundaries[i]
        r2 = r_boundaries[i + 1]

        # Phase twist along spiral angle
        twist_offset = i * 4.5  # degrees twist per ring

        for j in range(num_sectors):
            theta1 = j * sector_angle + twist_offset
            theta2 = theta1 + sector_angle

            # Alternating black/white fill with phase twist
            fill_color = "black" if (i + j) % 2 == 0 else "white"

            wedge = Wedge(
                (0, 0),
                r2,
                theta1,
                theta2,
                width=r2 - r1,
                facecolor=fill_color,
                edgecolor="black",
                linewidth=0.8,
            )
            ax.add_patch(wedge)

    # Superimpose concentric high-contrast radial rings to enhance illusory depth movement
    for r in np.linspace(5, 45, 9):
        circle = plt.Circle(
            (0, 0), r, fill=False, edgecolor="black", linewidth=2.0
        )
        ax.add_patch(circle)

    save(
        fig,
        "abstract optical radial vortex depth distortion illusion pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_radial_vortex_depth_distortion_illusion_pattern_black_white_texture()
