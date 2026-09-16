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
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name}_{DATE}.jpg"
    svg_path = SVG_DIR / f"{name}_{DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def herringbone_amplitude_gradient():
    """Tweak: chevron amplitude ramps left to right, flat ridges rising into tall peaks"""
    fig, ax = setup_ax()
    spacing = 4.0
    for y in np.arange(-6, 106, spacing):
        for x in np.arange(-6, 106, spacing * 2):
            amp = 0.8 + 6.0 * ((x + 6) / 112)
            lw = 0.9 + 0.5 * ((x + 6) / 112)
            ax.plot([x, x + spacing], [y, y + amp], color="black", linewidth=lw)
            ax.plot([x + spacing, x + spacing * 2], [y + amp, y], color="black", linewidth=lw)
    save(fig, "abstract_herringbone_amplitude_gradient_pattern_black_white_geometric_texture")


if __name__ == "__main__":
    herringbone_amplitude_gradient()
