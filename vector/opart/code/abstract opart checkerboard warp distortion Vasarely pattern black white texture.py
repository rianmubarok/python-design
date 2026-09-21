import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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
    """Generates a Vasarely style checkerboard warp."""
    fig, ax = setup_ax()
    
    grid_res = 30
    x = np.linspace(-1.2, 1.2, grid_res)
    y = np.linspace(-1.2, 1.2, grid_res)
    
    X, Y = np.meshgrid(x, y)
    
    # Distortion
    r = np.sqrt(X**2 + Y**2)
    distort = 1.0 - 0.6 * np.exp(-4 * r**2)
    
    Xd = X * distort
    Yd = Y * distort
    
    # Draw distorted checkerboard
    for i in range(grid_res - 1):
        for j in range(grid_res - 1):
            if (i + j) % 2 == 0:
                pts = np.array([
                    [Xd[i, j], Yd[i, j]],
                    [Xd[i, j+1], Yd[i, j+1]],
                    [Xd[i+1, j+1], Yd[i+1, j+1]],
                    [Xd[i+1, j], Yd[i+1, j]]
                ])
                poly = Polygon(pts, closed=True, facecolor="black", edgecolor="black", linewidth=0.2)
                ax.add_patch(poly)

    save(fig, "abstract opart checkerboard warp distortion Vasarely pattern black white texture")

if __name__ == "__main__":
    generate()
