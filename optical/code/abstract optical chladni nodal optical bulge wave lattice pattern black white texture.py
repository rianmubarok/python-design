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


def abstract_optical_chladni_nodal_optical_bulge_wave_lattice_pattern_black_white_texture():
    """Optical experiment: Chladni acoustic resonance nodal patterns merged with Op-Art lens bulge isolines."""
    fig, ax = setup_ax()

    # Create grid mesh for Chladni 2D nodal isolines
    res = 500
    x = np.linspace(-50, 50, res)
    y = np.linspace(-50, 50, res)
    X, Y = np.meshgrid(x, y)

    # Chladni mode numbers (n, m)
    n1, m1 = 3, 5
    L = 50.0

    # Chladni formula: cos(n*pi*x/L)*cos(m*pi*y/L) - cos(m*pi*x/L)*cos(n*pi*y/L)
    Z1 = np.cos(n1 * np.pi * X / L) * np.cos(m1 * np.pi * Y / L) - np.cos(
        m1 * np.pi * X / L
    ) * np.cos(n1 * np.pi * Y / L)

    # Superimpose secondary mode (n2, m2) = (4, 2)
    n2, m2 = 4, 2
    Z2 = np.cos(n2 * np.pi * X / L) * np.cos(m2 * np.pi * Y / L) - np.cos(
        m2 * np.pi * X / L
    ) * np.cos(n2 * np.pi * Y / L)

    Z_combined = Z1 * 0.6 + Z2 * 0.4

    # Add 3D lens bulge optical displacement to Z_combined
    R = np.sqrt(X**2 + Y**2)
    lens_mask = R < 42.0
    Z_combined[lens_mask] += 0.45 * (1.0 - (R[lens_mask] / 42.0) ** 2)

    # Plot crisp contour isolines
    levels = np.linspace(-1.2, 1.2, 32)
    ax.contour(
        X,
        Y,
        Z_combined,
        levels=levels,
        colors="black",
        linewidths=1.5,
    )

    save(
        fig,
        "abstract optical chladni nodal optical bulge wave lattice pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_chladni_nodal_optical_bulge_wave_lattice_pattern_black_white_texture()
