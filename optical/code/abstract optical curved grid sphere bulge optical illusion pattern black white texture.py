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


def abstract_optical_curved_grid_sphere_bulge_optical_illusion_pattern_black_white_texture():
    """Tweak: Grid distorted in 3D sphere bulge with line density gradient."""
    fig, ax = setup_ax()
    
    n_lines = 60
    grid_pts = np.linspace(-1, 1, 400)
    
    # Vertical grid lines
    for i in range(n_lines + 1):
        x0 = -1 + (2 * i / n_lines)
        y_vals = grid_pts
        
        r = np.sqrt(x0**2 + y_vals**2)
        distort = 1.0 - 0.65 * np.exp(-4 * r**2)
        
        x_dist = x0 * distort
        y_dist = y_vals * distort
        
        lw = 0.4 + 1.8 * np.exp(-4 * x0**2)
        ax.plot(x_dist, y_dist, color="black", linewidth=lw)
        
    # Horizontal grid lines
    for i in range(n_lines + 1):
        y0 = -1 + (2 * i / n_lines)
        x_vals = grid_pts
        
        r = np.sqrt(x_vals**2 + y0**2)
        distort = 1.0 - 0.65 * np.exp(-4 * r**2)
        
        x_dist = x_vals * distort
        y_dist = y0 * distort
        
        lw = 0.4 + 1.8 * np.exp(-4 * y0**2)
        ax.plot(x_dist, y_dist, color="black", linewidth=lw)

    save(fig, "abstract optical curved grid sphere bulge optical illusion pattern black white texture")


if __name__ == "__main__":
    abstract_optical_curved_grid_sphere_bulge_optical_illusion_pattern_black_white_texture()
