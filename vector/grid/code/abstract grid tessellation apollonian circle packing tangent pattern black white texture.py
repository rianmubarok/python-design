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
    Apollonian Circle Packing.
    A pseudo circle-packing algorithm on a grid to create a dense texture
    of perfectly tangent circles of varying radii.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.patches as patches

    # We use a brute force algorithm to pack circles.
    # We keep an array of available spaces.
    
    circles = [] # list of (x, y, r)
    
    # Try to add N circles
    for _ in range(5000):
        # Pick random point
        x = rng.uniform(-5, 105)
        y = rng.uniform(-5, 105)
        
        # Calculate max radius before hitting another circle
        max_r = 15.0 # cap radius
        valid = True
        
        for cx, cy, cr in circles:
            dist = np.sqrt((x - cx)**2 + (y - cy)**2)
            # Distance from point to edge of circle
            available_space = dist - cr
            
            if available_space <= 0.2:
                # Inside or too close to another circle
                valid = False
                break
                
            if available_space < max_r:
                max_r = available_space
                
        if valid and max_r > 0.5: # Minimum radius threshold
            circles.append((x, y, max_r))
            
            # Alternate thick outlines, fills, and target-like inner circles
            style = rng.choice([0, 1, 2, 3])
            
            if style == 0:
                # Solid fill
                c = patches.Circle((x, y), max_r - 0.2, facecolor='black', edgecolor='none')
                ax.add_patch(c)
            elif style == 1:
                # Thick outline
                c = patches.Circle((x, y), max_r - 0.2, facecolor='none', edgecolor='black', linewidth=1.5)
                ax.add_patch(c)
            elif style == 2:
                # Outline with dot
                c = patches.Circle((x, y), max_r - 0.2, facecolor='none', edgecolor='black', linewidth=0.5)
                ax.add_patch(c)
                dot = patches.Circle((x, y), max_r * 0.2, facecolor='black', edgecolor='none')
                ax.add_patch(dot)
            else:
                # Concentric
                c1 = patches.Circle((x, y), max_r - 0.2, facecolor='none', edgecolor='black', linewidth=1.0)
                c2 = patches.Circle((x, y), max_r * 0.5 - 0.1, facecolor='none', edgecolor='black', linewidth=1.0)
                ax.add_patch(c1)
                ax.add_patch(c2)

    save(fig, "abstract grid tessellation apollonian circle packing tangent pattern black white texture")


if __name__ == "__main__":
    draw()
