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
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
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


def abstract_sound_chladni_plate_nodal_vibration_pattern_black_white_texture():
    """Generates Chladni plate standing wave nodal lines."""
    fig, ax = setup_ax()
    
    # Grid of points
    grid_size = 600
    x = np.linspace(-1, 1, grid_size)
    y = np.linspace(-1, 1, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Chladni 2D wave equation parameters (modes n, m)
    n1, m1 = 3, 5
    n2, m2 = 5, 7
    
    # Superposition of standing wave modes
    L = 1.0
    Z1 = a_mode = np.cos(n1 * np.pi * X / L) * np.cos(m1 * np.pi * Y / L) - np.cos(m1 * np.pi * X / L) * np.cos(n1 * np.pi * Y / L)
    Z2 = b_mode = np.cos(n2 * np.pi * X / L) * np.cos(m2 * np.pi * Y / L) - np.cos(m2 * np.pi * X / L) * np.cos(n2 * np.pi * Y / L)
    
    Z = Z1 + 0.7 * Z2
    
    # Render contour lines where vibration amplitude is near nodal lines (Z approx 0)
    levels = np.linspace(-1.5, 1.5, 35)
    ax.contour(X, Y, Z, levels=levels, colors='black', linewidths=1.2)
    
    save(fig, "abstract sound chladni plate nodal vibration pattern black white texture")


if __name__ == "__main__":
    abstract_sound_chladni_plate_nodal_vibration_pattern_black_white_texture()
