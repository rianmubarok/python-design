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


def abstract_grid_tessellation_triangular_star_burst_grid_shift_pattern_black_white_texture():
    """Tweak: Star-burst node grid scaling radially from canvas center."""
    fig, ax = setup_ax()
    
    n_cols = 10
    n_rows = 10
    dx = 100 / n_cols
    dy = 100 / n_rows
    
    for r in range(n_rows):
        for c in range(n_cols):
            cx = (c + 0.5) * dx
            cy = (r + 0.5) * dy
            
            # Distance from center (50, 50)
            dist = np.sqrt((cx - 50)**2 + (cy - 50)**2)
            star_radius = 4.5 * np.exp(-dist * 0.02)
            
            # Draw 8-point star rays
            n_rays = 8
            for k in range(n_rays):
                angle = k * 2 * np.pi / n_rays
                x_end = cx + star_radius * np.cos(angle)
                y_end = cy + star_radius * np.sin(angle)
                ax.plot([cx, x_end], [cy, y_end], color="black", linewidth=1.2)
                
            # Connecting outer square boundary
            ax.plot([cx - dx/2, cx + dx/2, cx + dx/2, cx - dx/2, cx - dx/2],
                    [cy - dy/2, cy - dy/2, cy + dy/2, cy + dy/2, cy - dy/2],
                    color="black", linewidth=0.5, alpha=0.5)

    save(fig, "abstract grid tessellation triangular star burst grid shift pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_triangular_star_burst_grid_shift_pattern_black_white_texture()
