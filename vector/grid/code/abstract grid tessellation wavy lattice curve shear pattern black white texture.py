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
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def abstract_grid_tessellation_wavy_lattice_curve_shear_pattern_black_white_texture():
    """Tweak: Square grid sheared vertically and horizontally by perpendicular sine waves."""
    fig, ax = setup_ax()
    
    n_lines = 40
    pts = np.linspace(0, 100, 300)
    
    # Vertical grid lines warped by y-sine
    x_coords = np.linspace(0, 100, n_lines)
    for x0 in x_coords:
        x_warped = x0 + 4.0 * np.sin(pts * 0.1)
        y_warped = pts
        ax.plot(x_warped, y_warped, color="black", linewidth=1.0)
        
    # Horizontal grid lines warped by x-sine
    y_coords = np.linspace(0, 100, n_lines)
    for y0 in y_coords:
        x_warped = pts
        y_warped = y0 + 4.0 * np.sin(pts * 0.1)
        ax.plot(x_warped, y_warped, color="black", linewidth=1.0)

    save(fig, "abstract grid tessellation wavy lattice curve shear pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_wavy_lattice_curve_shear_pattern_black_white_texture()
