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
    Isometric Impossible Stairs / Escher blocks.
    Draws a grid of isometric cubes arranged in staggered heights, creating
    an optical illusion of complex staircases.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    cube_size = 3.5
    h = cube_size * np.sqrt(3) / 2.0
    
    cols = 25
    rows = 25

    # Face definitions for origin (0,0)
    p1 = np.array([0, cube_size])
    p2 = np.array([cube_size * np.cos(np.pi/6), cube_size * np.sin(np.pi/6)])
    p3 = np.array([cube_size * np.cos(np.pi/6), -cube_size * np.sin(np.pi/6)])
    p4 = np.array([0, -cube_size])
    p5 = np.array([-cube_size * np.cos(np.pi/6), -cube_size * np.sin(np.pi/6)])
    p6 = np.array([-cube_size * np.cos(np.pi/6), cube_size * np.sin(np.pi/6)])
    center = np.array([0, 0])

    face_top = [center, p1, p2, p3, center]
    face_left = [center, p3, p4, p5, center]
    face_right = [center, p5, p6, p1, center]

    import matplotlib.patches as patches
    
    # Generate a height map
    heights = np.zeros((rows, cols))
    for r in range(rows):
        for c in range(cols):
            # Perlin-like simple waves for stair structures
            heights[r, c] = int((np.sin(r * 0.5) + np.cos(c * 0.5)) * 3)

    # To draw correctly in isometric, we must sort by depth (back to front)
    # y determines depth. Top of the screen is back, bottom is front.
    # So we draw from row 0 down, and within a row, left to right.
    
    for row in reversed(range(rows)):
        for col in range(cols):
            cx = (col * 1.5) * cube_size - 10
            # Offset y by row, and stagger odd columns
            cy = (row * 2.0) * h - 10
            if col % 2 != 0:
                cy += h
                
            # Add height (z-axis in iso is just vertical translation on screen)
            z_offset = heights[row, col] * cube_size
            cy += z_offset
            
            top_poly = patches.Polygon(np.array(face_top) + [cx, cy], closed=True, 
                                      facecolor='white', edgecolor='black', linewidth=1.5)
            left_poly = patches.Polygon(np.array(face_left) + [cx, cy], closed=True, 
                                      facecolor='black', edgecolor='black', linewidth=1.5)
            # Use tight hatching for right face
            right_poly = patches.Polygon(np.array(face_right) + [cx, cy], closed=True, 
                                      facecolor='none', edgecolor='black', linewidth=1.5, hatch='\\\\\\\\')
                                      
            ax.add_patch(top_poly)
            ax.add_patch(left_poly)
            ax.add_patch(right_poly)
            
            # Optionally draw columns connecting down to a base so it looks solid
            # but floating stairs look more abstract and Escher-like!

    save(fig, "abstract grid tessellation isometric impossible stairs pattern black white texture")


if __name__ == "__main__":
    draw()
