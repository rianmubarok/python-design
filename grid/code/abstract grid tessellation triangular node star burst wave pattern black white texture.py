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


def abstract_grid_tessellation_triangular_node_star_burst_wave_pattern_black_white_texture():
    """Tweak: Triangular grid with star node sizes modulating according to a 2D sine wave."""
    fig, ax = setup_ax()
    
    a = 10.0
    h = a * np.sqrt(3) / 2
    
    n_cols = 12
    n_rows = 12
    
    for r in range(n_rows):
        for c in range(n_cols):
            cx = c * a
            if r % 2 != 0:
                cx += a / 2
            cy = r * h
            
            # Star size modulated by 2D sine wave
            star_radius = 2.0 + 2.5 * (0.5 * (1 + np.sin(cx * 0.1) * np.cos(cy * 0.1)))
            
            # Draw 6-point star at node
            for k in range(6):
                angle = k * np.pi / 3
                x_end = cx + star_radius * np.cos(angle)
                y_end = cy + star_radius * np.sin(angle)
                ax.plot([cx, x_end], [cy, y_end], color="black", linewidth=1.0)
                
            # Connecting triangle edges
            if c < n_cols - 1:
                ax.plot([cx, cx + a], [cy, cy], color="black", linewidth=0.5, alpha=0.5)

    save(fig, "abstract grid tessellation triangular node star burst wave pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_triangular_node_star_burst_wave_pattern_black_white_texture()
