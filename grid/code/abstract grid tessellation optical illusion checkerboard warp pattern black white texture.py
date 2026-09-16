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
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


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


def draw():
    """
    Optical Illusion Checkerboard Warp.
    A standard checkerboard grid that is heavily warped by sine waves,
    creating a bulging 3D sphere or ripple illusion (like Vasarely's Vega).
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches
    
    n_cells = 40
    cell_size = 120.0 / n_cells
    
    # Create the grid points
    grid_x = np.linspace(-10, 110, n_cells + 1)
    grid_y = np.linspace(-10, 110, n_cells + 1)
    
    X, Y = np.meshgrid(grid_x, grid_y)
    
    # Warp the coordinates
    cx, cy = 50.0, 50.0
    DX = X - cx
    DY = Y - cy
    R = np.sqrt(DX**2 + DY**2)
    
    # Lens distortion: pull points outward around the center
    # This creates a spherical bulge effect
    mag = 1.0 + 30.0 * np.exp(-(R**2)/800.0)
    
    X_warped = cx + (DX / (R + 1e-5)) * mag * (R**0.8)
    Y_warped = cy + (DY / (R + 1e-5)) * mag * (R**0.8)

    # Draw the distorted checkerboard squares
    for i in range(n_cells):
        for j in range(n_cells):
            # Only draw black squares
            if (i + j) % 2 == 0:
                p1 = [X_warped[i, j], Y_warped[i, j]]
                p2 = [X_warped[i, j+1], Y_warped[i, j+1]]
                p3 = [X_warped[i+1, j+1], Y_warped[i+1, j+1]]
                p4 = [X_warped[i+1, j], Y_warped[i+1, j]]
                
                poly = patches.Polygon([p1, p2, p3, p4], closed=True, 
                                      facecolor='black', edgecolor='none')
                ax.add_patch(poly)

    save(fig, "abstract grid tessellation optical illusion checkerboard warp pattern black white texture")


if __name__ == "__main__":
    draw()
