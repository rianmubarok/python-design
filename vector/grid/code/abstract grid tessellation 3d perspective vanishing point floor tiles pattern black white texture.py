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
    3D Perspective Vanishing Point Floor Tiles.
    A simple checkerboard floor distorted heavily by 3D perspective to simulate
    an infinite plane converging at a vanishing point.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches
    
    # We define a grid in 3D and project it.
    n_cols = 40
    n_depth = 50
    
    # Horizon line
    horizon_y = 75.0
    
    # Floor goes from y = -20 to horizon_y
    # In 3D space, X is left/right, Z is depth
    x_grid = np.linspace(-300, 400, n_cols)
    z_grid = np.geomspace(1, 400, n_depth) # Geometric spacing makes the perspective realistic
    
    vanishing_x = 50.0
    
    # Draw horizontal lines (depth)
    for i in range(len(z_grid)):
        z = z_grid[i]
        # Calculate Y position on screen
        # As z increases, y approaches horizon
        screen_y = horizon_y - (100.0 / z)
        
        # Calculate screen X bounds
        left_x = vanishing_x + (x_grid[0] - vanishing_x) / z
        right_x = vanishing_x + (x_grid[-1] - vanishing_x) / z
        
        ax.plot([left_x, right_x], [screen_y, screen_y], color="black", linewidth=0.8)
        
    # Draw vertical lines (converging to vanishing point)
    for x in x_grid:
        bottom_x = vanishing_x + (x - vanishing_x) / z_grid[0]
        bottom_y = horizon_y - (100.0 / z_grid[0])
        
        top_x = vanishing_x + (x - vanishing_x) / z_grid[-1]
        top_y = horizon_y - (100.0 / z_grid[-1])
        
        ax.plot([bottom_x, top_x], [bottom_y, top_y], color="black", linewidth=0.8)
        
    # Fill alternating tiles to make a checkerboard
    for i in range(len(z_grid) - 1):
        for j in range(len(x_grid) - 1):
            if (i + j) % 2 == 0:
                z1 = z_grid[i]
                z2 = z_grid[i+1]
                
                y1 = horizon_y - (100.0 / z1)
                y2 = horizon_y - (100.0 / z2)
                
                x1_bottom = vanishing_x + (x_grid[j] - vanishing_x) / z1
                x2_bottom = vanishing_x + (x_grid[j+1] - vanishing_x) / z1
                
                x1_top = vanishing_x + (x_grid[j] - vanishing_x) / z2
                x2_top = vanishing_x + (x_grid[j+1] - vanishing_x) / z2
                
                poly = patches.Polygon([
                    [x1_bottom, y1], [x2_bottom, y1], [x2_top, y2], [x1_top, y2]
                ], closed=True, facecolor='black', edgecolor='black', linewidth=0.5)
                ax.add_patch(poly)

    save(fig, "abstract grid tessellation 3d perspective vanishing point floor tiles pattern black white texture")


if __name__ == "__main__":
    draw()
