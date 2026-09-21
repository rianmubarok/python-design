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

def generate():
    """Generates an op-art grid with multiple bulging spheres."""
    fig, ax = setup_ax()
    
    n_lines = 100
    grid_pts = np.linspace(-1.5, 1.5, 1000)
    
    centers = [(0.5, 0.5), (-0.4, 0.3), (0.2, -0.6), (-0.7, -0.5)]
    
    def apply_distortion(x, y):
        x_new, y_new = np.copy(x), np.copy(y)
        total_distort_x = np.zeros_like(x)
        total_distort_y = np.zeros_like(y)
        
        for cx, cy in centers:
            r = np.sqrt((x - cx)**2 + (y - cy)**2)
            distort = 0.5 * np.exp(-5 * r**2)
            total_distort_x += (x - cx) * distort
            total_distort_y += (y - cy) * distort
            
        return x - total_distort_x, y - total_distort_y
    
    for i in range(n_lines + 1):
        x0 = -1.5 + (3 * i / n_lines)
        y_vals = grid_pts
        
        x_dist, y_dist = apply_distortion(np.full_like(y_vals, x0), y_vals)
        ax.plot(x_dist, y_dist, color="black", linewidth=0.8)
        
    for i in range(n_lines + 1):
        y0 = -1.5 + (3 * i / n_lines)
        x_vals = grid_pts
        
        x_dist, y_dist = apply_distortion(x_vals, np.full_like(x_vals, y0))
        ax.plot(x_dist, y_dist, color="black", linewidth=0.8)

    save(fig, "abstract opart bulging multiple spheres grid distortion pattern black white texture")

if __name__ == "__main__":
    generate()
