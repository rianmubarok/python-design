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
    Woven Chainmail Interlocking Rings.
    A dense grid simulating medieval chainmail armor by layering thousands
    of interlocking rings.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches

    # European 4-in-1 chainmail weave
    # Rings are laid out in staggered rows.
    # Rings slant in alternating directions row by row.
    
    radius = 3.0
    # Horizontal spacing is tighter than radius to allow overlap
    dx = radius * 1.5
    # Vertical spacing
    dy = radius * 1.0
    
    cols = int(120 / dx) + 2
    rows = int(120 / dy) + 2
    
    # We draw rows from top to bottom.
    # To create the 3D interlocking illusion in 2D vector art without actual 3D z-buffering:
    # We draw thick black rings, then a slightly smaller white ring inside to make an outline,
    # and use layering.
    
    for row in range(-2, rows):
        for col in range(-2, cols):
            cx = -10 + col * dx
            cy = 110 - row * dy
            
            if row % 2 != 0:
                cx += dx / 2
                
            # Simulate slant by drawing an ellipse instead of a perfect circle
            # Row slant alternates
            angle = 20 if row % 2 == 0 else -20
            
            # Thick black background ring
            e_bg = patches.Ellipse((cx, cy), radius * 2.2, radius * 1.4, angle=angle,
                                   facecolor='black', edgecolor='none', zorder=row)
            # Inner white cutout
            e_fg = patches.Ellipse((cx, cy), radius * 1.6, radius * 0.8, angle=angle,
                                   facecolor='white', edgecolor='none', zorder=row)
                                   
            ax.add_patch(e_bg)
            ax.add_patch(e_fg)
            
            # To make the 4-in-1 overlap work perfectly, we would need to split the rings
            # into upper/lower halves and z-order them. 
            # Alternatively, drawing them compactly with high overlap creates an abstract weave texture.
            # Adding a center dot enhances the metal loop illusion
            dot = patches.Circle((cx, cy), radius * 0.2, facecolor='black', edgecolor='none', zorder=row)
            ax.add_patch(dot)

    save(fig, "abstract grid tessellation woven chainmail interlocking rings pattern black white texture")


if __name__ == "__main__":
    draw()
