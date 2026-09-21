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
    Isometric Cube Tessellation (Q*bert style).
    A grid of repeating 3D isometric cubes that form a continuous tiling pattern.
    """
    fig, ax = setup_ax()

    cube_size = 4.0
    h = cube_size * np.sqrt(3) / 2.0
    
    # Calculate grid range
    cols = int(120 / (cube_size * 1.5)) + 2
    rows = int(120 / h) + 2

    # Pre-calculate the 3 visible faces of an isometric cube (represented as polygons)
    # Origin at center of cube
    center = np.array([0, 0])
    p1 = np.array([0, cube_size])
    p2 = np.array([cube_size * np.cos(np.pi/6), cube_size * np.sin(np.pi/6)])
    p3 = np.array([cube_size * np.cos(np.pi/6), -cube_size * np.sin(np.pi/6)])
    p4 = np.array([0, -cube_size])
    p5 = np.array([-cube_size * np.cos(np.pi/6), -cube_size * np.sin(np.pi/6)])
    p6 = np.array([-cube_size * np.cos(np.pi/6), cube_size * np.sin(np.pi/6)])

    face_top = [center, p1, p2, p3, center]
    face_left = [center, p3, p4, p5, center]
    face_right = [center, p5, p6, p1, center]

    import matplotlib.patches as patches
    
    for row in range(-2, rows):
        for col in range(-2, cols):
            # Hexagonal/Isometric staggering
            cx = col * cube_size * 1.5
            cy = row * h * 2.0
            if col % 2 != 0:
                cy += h
                
            # Draw the 3 faces with different hatchings or fills to simulate shading
            # Top face (lightest)
            top_poly = patches.Polygon(np.array(face_top) + [cx, cy], closed=True, 
                                      facecolor='white', edgecolor='black', linewidth=1.5)
            # Left face (medium)
            left_poly = patches.Polygon(np.array(face_left) + [cx, cy], closed=True, 
                                      facecolor='none', edgecolor='black', linewidth=1.5, hatch='///')
            # Right face (darkest)
            right_poly = patches.Polygon(np.array(face_right) + [cx, cy], closed=True, 
                                      facecolor='black', edgecolor='black', linewidth=1.5)
                                      
            ax.add_patch(top_poly)
            ax.add_patch(left_poly)
            ax.add_patch(right_poly)

    save(fig, "abstract grid tessellation isometric cube pattern black white texture")


if __name__ == "__main__":
    draw()
