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


def abstract_optical_fraser_spiral_twisted_cord_concentric_pattern_black_white_texture():
    """Optical experiment: Fraser spiral illusion built from concentric rings of tilted cord elements."""
    fig, ax = setup_ax()

    num_rings = 18
    radii = np.linspace(4, 46, num_rings)

    # Draw faint guide concentric circles
    for r in radii:
        circle = plt.Circle(
            (0, 0), r, fill=False, edgecolor="black", linewidth=0.6, alpha=0.4
        )
        ax.add_patch(circle)

    # Add twisted cord segments tilted at ~18 degrees relative to tangent
    tilt_angle = np.radians(22)  # inward tilt

    for idx, r in enumerate(radii):
        # Number of cord elements increases with radius
        num_elements = int(24 + idx * 8)
        angles = np.linspace(0, 2 * np.pi, num_elements, endpoint=False)
        segment_len = 2.4 + idx * 0.15

        for a in angles:
            cx = r * np.cos(a)
            cy = r * np.sin(a)

            # Tangent angle + inward tilt angle
            tangent = a + np.pi / 2
            cord_dir = tangent + tilt_angle

            dx = (segment_len / 2) * np.cos(cord_dir)
            dy = (segment_len / 2) * np.sin(cord_dir)

            # Draw dark bold cord stroke
            ax.plot(
                [cx - dx, cx + dx],
                [cy - dy, cy + dy],
                color="black",
                linewidth=2.8,
            )

            # Draw white core highlight along the cord to enhance twisted fiber illusion
            ax.plot(
                [cx - dx * 0.5, cx + dx * 0.5],
                [cy - dy * 0.5, cy + dy * 0.5],
                color="white",
                linewidth=1.0,
            )

    save(
        fig,
        "abstract optical fraser spiral twisted cord concentric pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_fraser_spiral_twisted_cord_concentric_pattern_black_white_texture()
