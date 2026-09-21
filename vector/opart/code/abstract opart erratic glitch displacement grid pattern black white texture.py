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
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
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
    """Generates an erratic grid that flows like a glitchy liquid."""
    fig, ax = setup_ax()
    
    n_lines = 80
    grid_pts = np.linspace(0, 1, 300)
    
    def glitch_displacement(x, y):
        # Fake perlin noise using multiple sine/cosine waves
        dx = 0.02 * np.sin(20 * x) * np.cos(15 * y) + 0.01 * np.sin(40 * y + 10 * x)
        dy = 0.02 * np.cos(18 * y) * np.sin(25 * x) + 0.01 * np.cos(35 * x + 15 * y)
        
        # Add random jaggedness based on sine threshold
        glitch = np.where(np.sin(100 * x * y) > 0.8, 0.01, 0)
        return x + dx + glitch, y + dy + glitch
    
    # Verticals
    for i in range(n_lines + 1):
        x0 = i / n_lines
        y_vals = grid_pts
        x_vals = np.full_like(y_vals, x0)
        
        x_dist, y_dist = glitch_displacement(x_vals, y_vals)
        ax.plot(x_dist, y_dist, color="black", linewidth=1.2)
        
    # Horizontals
    for i in range(n_lines + 1):
        y0 = i / n_lines
        x_vals = grid_pts
        y_vals = np.full_like(x_vals, y0)
        
        x_dist, y_dist = glitch_displacement(x_vals, y_vals)
        ax.plot(x_dist, y_dist, color="black", linewidth=1.2)

    save(fig, "abstract opart erratic glitch displacement grid pattern black white texture")

if __name__ == "__main__":
    generate()
