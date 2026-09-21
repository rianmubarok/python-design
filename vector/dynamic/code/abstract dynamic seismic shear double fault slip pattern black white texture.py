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


def abstract_dynamic_seismic_shear_double_fault_slip_pattern_black_white_texture():
    """Tweak: Multiple intersecting fault lines causing dynamic offset displacements."""
    fig, ax = setup_ax()
    
    n_lines = 45
    y_vals = np.linspace(5, 95, n_lines)
    
    for y0 in y_vals:
        x_pts = np.linspace(0, 100, 500)
        y_pts = np.full_like(x_pts, y0)
        
        # Dual intersecting faults
        fault1 = (x_pts > 25) & (x_pts < 50)
        fault2 = (x_pts > 50) & (x_pts < 75)
        
        y_pts[fault1] += 3.0 * np.sin(y0 * 0.15)
        y_pts[fault2] -= 3.0 * np.cos(y0 * 0.15)
        
        ax.plot(x_pts, y_pts, color="black", linewidth=0.9)

    save(fig, "abstract dynamic seismic shear double fault slip pattern black white texture")


if __name__ == "__main__":
    abstract_dynamic_seismic_shear_double_fault_slip_pattern_black_white_texture()
