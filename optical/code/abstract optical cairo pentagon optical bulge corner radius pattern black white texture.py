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


def bulge_transform(pts, radius=42.0, strength=1.4):
    """Apply radial optical bulge deformation to array of 2D points."""
    bulged = []
    for x, y in pts:
        d = np.sqrt(x**2 + y**2)
        if d < radius:
            f = 1.0 + strength * (1.0 - (d / radius) ** 2)
        else:
            f = 1.0
        bulged.append([x * f, y * f])
    return np.array(bulged)


def abstract_optical_cairo_pentagon_optical_bulge_corner_radius_pattern_black_white_texture():
    """Optical experiment: Cairo pentagonal tiling with non-linear radial lens bulge and vertex pinch."""
    fig, ax = setup_ax()

    # Generate standard Cairo pentagon base tile template vertices
    a = 7.5
    # Base pentagon template
    base_pentagon = np.array(
        [[0, 0], [a, 0], [a + a / 2, a * np.sqrt(3) / 2], [a / 2, a + a * np.sqrt(3) / 2], [0, a]]
    )

    # Replicate Cairo pentagons over grid
    n_tiles = 7
    offsets = np.linspace(-38, 38, n_tiles)

    for i, ox in enumerate(offsets):
        for j, oy in enumerate(offsets):
            for rotate_idx in range(4):
                # Rotate pentagon template
                theta = rotate_idx * np.pi / 2
                c, s = np.cos(theta), np.sin(theta)
                R = np.array([[c, -s], [s, c]])

                transformed = base_pentagon @ R.T + np.array([ox, oy])

                # Apply optical bulge transform
                bulged_pts = bulge_transform(transformed)

                fill_val = (i + j + rotate_idx) % 2 == 0

                poly = Polygon(
                    bulged_pts,
                    closed=True,
                    facecolor="black" if fill_val else "white",
                    edgecolor="black",
                    linewidth=1.2,
                )
                ax.add_patch(poly)

    save(
        fig,
        "abstract optical cairo pentagon optical bulge corner radius pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_cairo_pentagon_optical_bulge_corner_radius_pattern_black_white_texture()
