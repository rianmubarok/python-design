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
    Houndstooth Textile Weave.
    A mathematically accurate generation of the classic houndstooth 
    tessellation pattern, often found in vintage fabrics.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches
    
    scale = 3.5
    cols = int(120 / (scale * 2)) + 1
    rows = int(120 / (scale * 2)) + 1

    # Base shape of a single houndstooth block
    # A houndstooth consists of a central square and four triangles 
    # attached to corners/edges in a specific pinwheel formation.
    
    # We will build it by combining polygons
    center = np.array([0, 0])
    
    # The classic houndstooth shape (centered at 0,0)
    # It tiles on a square grid rotated by 45 degrees.
    p = np.array([
        [-1, 1],   # top left
        [0, 1],    # top mid
        [0, 2],    # spike up
        [1, 1],    # spike down
        [1, 0],    # right mid
        [2, 0],    # spike right
        [1, -1],   # spike left
        [0, -1],   # bot mid
        [-1, -2],  # long tail bot left
        [-1, -1],  
        [-2, -1],  # long tail left bot
        [-1, 0]    
    ]) * scale
    
    # Shift and draw across the grid
    for row in range(-2, rows):
        for col in range(-2, cols):
            # Diagonal stepping
            cx = (col * 2 + (row % 2)) * scale
            cy = row * scale * 2
            
            # The pattern consists of solid black tiles
            poly = patches.Polygon(p + [cx, cy], closed=True, 
                                  facecolor='black', edgecolor='black', linewidth=0.5, joinstyle='miter')
            ax.add_patch(poly)
            
            # Draw tiny inner diagonal lines (texture) inside the white spaces for an abstract twist
            wx = cx + scale
            wy = cy
            ax.plot([wx-scale/2, wx+scale/2], [wy-scale/2, wy+scale/2], color='black', linewidth=1.5)

    save(fig, "abstract grid tessellation houndstooth textile weave pattern black white texture")


if __name__ == "__main__":
    draw()
