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
    Optical Illusion Hermann Grid Distortion.
    The classic Hermann Grid illusion (black squares with white gutters causing
    ghostly grey spots at the intersections), distorted by a radial lens effect.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches
    
    # We create a dense array of black squares
    grid_size = 40
    cell_w = 120.0 / grid_size
    gap = cell_w * 0.25 # The white gutter
    
    for row in range(grid_size):
        for col in range(grid_size):
            cx = -10 + col * cell_w
            cy = -10 + row * cell_w
            
            # Apply a geometric spherical distortion (Bulge effect)
            # Find vector from center
            dx = cx - 50.0
            dy = cy - 50.0
            dist = np.sqrt(dx**2 + dy**2)
            
            # Distortion factor (lens effect)
            if dist < 45.0:
                # Bulge outward
                factor = 1.0 + 0.8 * np.cos(dist / 45.0 * np.pi/2)
            else:
                factor = 1.0
                
            # The trick is to distort the *size* and *position* of the squares
            # while maintaining the gap ratio.
            
            # To do this accurately without warping the actual polygon shape (which is hard),
            # we just scale the square size and gap based on distance, and offset the center.
            
            new_cx = 50.0 + dx * (1.0 + 0.3 * np.cos(dist / 60.0 * np.pi/2))
            new_cy = 50.0 + dy * (1.0 + 0.3 * np.cos(dist / 60.0 * np.pi/2))
            
            square_size = (cell_w - gap) * factor
            
            # The classic illusion needs sharp edges
            rect = patches.Rectangle((new_cx, new_cy), square_size, square_size, 
                                     facecolor='black', edgecolor='none')
            ax.add_patch(rect)
            
            # Add a tiny white dot in the center of the black square to make it pop
            if dist < 45.0:
                dot = patches.Circle((new_cx + square_size/2, new_cy + square_size/2), 
                                     square_size*0.05, facecolor='white', edgecolor='none')
                ax.add_patch(dot)

    save(fig, "abstract grid tessellation optical illusion hermann grid distortion pattern black white texture")


if __name__ == "__main__":
    draw()
