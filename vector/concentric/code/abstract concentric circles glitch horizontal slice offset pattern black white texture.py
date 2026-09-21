import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
EPS_DIR = OUTPUT_DIR / "eps"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


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
    eps_path = EPS_DIR / f"{name} {DATE}.eps"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    # Save EPS with larger figure size for 4MP+ bounding box
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format="eps", pad_inches=0, facecolor="white", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path} | {eps_path}")


def draw():
    """
    Glitch Horizontal Slice Offset.
    Concentric circles cut into horizontal bands, with each band
    randomly shifted left or right to simulate a VHS tracking glitch.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    cx, cy = 50.0, 50.0
    n_circles = 40
    max_radius = 65.0
    n_pts = 600

    # Define slice bands
    n_bands = 25
    band_edges = np.linspace(-5, 105, n_bands + 1)
    # Random shift for each band
    band_shifts = rng.uniform(-4.0, 4.0, n_bands)
    
    # We will generate the circle points and then offset their x based on their y
    for i in range(1, n_circles + 1):
        r = max_radius * (i / n_circles)
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        x = cx + r * np.cos(angles)
        y = cy + r * np.sin(angles)
        
        x_shifted = np.copy(x)
        
        for b in range(n_bands):
            y_min = band_edges[b]
            y_max = band_edges[b+1]
            mask = (y >= y_min) & (y < y_max)
            x_shifted[mask] += band_shifts[b]
            
        # To prevent long connecting lines across jumps, we can use a LineCollection or insert NaNs
        # Inserting NaNs at jump points
        diffs = np.abs(np.diff(x_shifted))
        jump_indices = np.where(diffs > 1.0)[0] + 1
        
        x_plot = np.insert(x_shifted, jump_indices, np.nan)
        y_plot = np.insert(y, jump_indices, np.nan)
        
        # Also need to close the circle if it didn't jump at the end
        if np.isnan(x_plot[-1]) == False and np.abs(x_plot[0] - x_plot[-1]) < 1.0:
            x_plot = np.append(x_plot, x_plot[0])
            y_plot = np.append(y_plot, y_plot[0])
            
        ax.plot(x_plot, y_plot, color="black", linewidth=1.5, solid_capstyle="butt")

    save(fig, "abstract concentric circles glitch horizontal slice offset pattern black white texture")


if __name__ == "__main__":
    draw()
