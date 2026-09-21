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
    """Optical experiment: Op-Art squircle grid with smooth radial lens bulging deformation."""
    fig, ax = setup_ax()

    grid_res = 22
    xs = np.linspace(-44, 44, grid_res)
    ys = np.linspace(-44, 44, grid_res)

    lens_radius = 45.0
    strength = 0.55  # Kekuatan distorsi disesuaikan agar transisi mulus

    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            dist = np.sqrt(x**2 + y**2)

            # Distorsi Cembung Lensa (Spherical bulge offset)
            if dist < lens_radius:
                # Transisi kurva halus (cosine-based smooth factor)
                factor = 1.0 + strength * (np.cos((dist / lens_radius) * (np.pi / 2)) ** 2)
            else:
                factor = 1.0

            wx = x * factor
            wy = y * factor

            # Ukuran dasar squircle dikontrol ketat agar tidak saling bertabrakan
            base_size = 3.2 * (0.85 + 0.3 * (factor - 1.0))

            # Morphing radius sudut: makin ke tengah makin bulat (squircle -> circle)
            corner_r = min(base_size * 0.45, max(0.3, 1.4 * (1.0 - dist / 60.0)))

            # Pola warna berselang-seling papan catur
            fill_val = (i + j) % 2 == 0

            patch = FancyBboxPatch(
                (wx - base_size / 2, wy - base_size / 2),
                base_size,
                base_size,
                boxstyle=f"round,pad=0,rounding_size={corner_r:.2f}",
                facecolor="black" if fill_val else "white",
                edgecolor="black",
                linewidth=1.0,
                zorder=2,
            )
            ax.add_patch(patch)

    save(
        fig,
        "abstract optical opart bulging squircle radius morph grid pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_opart_bulging_squircle_radius_morph_grid_pattern_black_white_texture()