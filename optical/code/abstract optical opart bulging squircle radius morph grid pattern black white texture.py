import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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


def abstract_optical_opart_bulging_squircle_radius_morph_grid_pattern_black_white_texture():
    """Optical experiment: Op-Art squircle grid with radial lens bulging deformation and dynamic corner morphing."""
    fig, ax = setup_ax()

    grid_res = 22
    xs = np.linspace(-45, 45, grid_res)
    ys = np.linspace(-45, 45, grid_res)

    lens_radius = 42.0
    strength = 1.45

    for x in xs:
        for y in ys:
            dist = np.sqrt(x**2 + y**2)

            if dist < lens_radius:
                # Spherical magnification / displacement
                factor = 1.0 + (strength * (1.0 - (dist / lens_radius) ** 2))
            else:
                factor = 1.0

            wx = x * factor
            wy = y * factor

            base_w = 3.2 * factor
            base_h = 3.2 * factor

            # Morph corner radius based on radial distance from center
            corner_r = max(0.2, min(base_w * 0.45, 1.4 * (1.0 - dist / 50.0)))

            # Fill condition alternates like checkerboard
            idx_x = int((x + 45) / 90 * grid_res)
            idx_y = int((y + 45) / 90 * grid_res)
            fill_val = (idx_x + idx_y) % 2 == 0

            patch = FancyBboxPatch(
                (wx - base_w / 2, wy - base_h / 2),
                base_w,
                base_h,
                boxstyle=f"round,pad=0,rounding_size={corner_r}",
                facecolor="black" if fill_val else "white",
                edgecolor="black",
                linewidth=1.2,
            )
            ax.add_patch(patch)

    save(
        fig,
        "abstract optical opart bulging squircle radius morph grid pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_opart_bulging_squircle_radius_morph_grid_pattern_black_white_texture()
