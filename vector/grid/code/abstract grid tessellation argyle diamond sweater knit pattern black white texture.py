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
    Argyle Diamond Sweater Knit.
    The classic Scottish Argyle pattern with overlapping diamonds and dashed intersecting lines.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches
    
    diamond_w = 12.0
    diamond_h = 24.0
    
    cols = int(120 / diamond_w) + 2
    rows = int(120 / diamond_h) + 2
    
    # Layer 1: Solid Diamonds
    for row in range(-1, rows):
        for col in range(-1, cols):
            cx = col * diamond_w
            cy = row * diamond_h
            if col % 2 != 0:
                cy += diamond_h / 2
                
            # Diamond polygon
            p = [
                [cx, cy + diamond_h/2],
                [cx + diamond_w/2, cy],
                [cx, cy - diamond_h/2],
                [cx - diamond_w/2, cy]
            ]
            
            # Alternate fill colors (black, white, and hatched for grey)
            style = (row + col) % 3
            if style == 0:
                poly = patches.Polygon(p, closed=True, facecolor='black', edgecolor='none')
            elif style == 1:
                poly = patches.Polygon(p, closed=True, facecolor='none', edgecolor='black', linewidth=1.5, hatch='////')
            else:
                poly = patches.Polygon(p, closed=True, facecolor='white', edgecolor='black', linewidth=1.0)
                
            ax.add_patch(poly)
            
    # Layer 2: Intersecting Dashed Lines (the signature Argyle thread)
    # These cross through the centers of the diamonds
    for row in range(-2, rows + 2):
        for col in range(-2, cols + 2):
            cx = col * diamond_w
            cy = row * diamond_h
            if col % 2 != 0:
                cy += diamond_h / 2
                
            # Draw X lines across the diamond
            ax.plot([cx - diamond_w/2, cx + diamond_w/2], 
                    [cy - diamond_h/2, cy + diamond_h/2], 
                    color="black", linewidth=2.5, linestyle=(0, (3, 3)))
                    
            ax.plot([cx - diamond_w/2, cx + diamond_w/2], 
                    [cy + diamond_h/2, cy - diamond_h/2], 
                    color="black", linewidth=2.5, linestyle=(0, (3, 3)))

    save(fig, "abstract grid tessellation argyle diamond sweater knit pattern black white texture")


if __name__ == "__main__":
    draw()
