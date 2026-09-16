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
    Triaxial Kagome Basket Weave Lattice.
    A grid made of intersecting triangles and hexagons, representing
    traditional Japanese Kagome basket weaving.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches
    
    scale = 6.0
    h = scale * np.sqrt(3) / 2.0
    
    cols = int(120 / (scale * 1.5)) + 2
    rows = int(120 / h) + 2

    for row in range(-2, rows):
        for col in range(-2, cols):
            cx = col * scale * 1.5
            cy = row * h * 2.0
            if col % 2 != 0:
                cy += h
                
            # Kagome lattice consists of overlapping David stars/hexagrams
            # We can draw it by simply placing 2 intersecting equilateral triangles
            # at each node to form the Star of David, creating the Kagome weave.
            
            # Triangle 1 (pointing up)
            r = scale * 0.8
            angles1 = np.array([90, 210, 330])
            rads1 = np.radians(angles1)
            x1 = cx + r * np.cos(rads1)
            y1 = cy + r * np.sin(rads1)
            
            poly1 = patches.Polygon(np.column_stack([x1, y1]), closed=True, 
                                   facecolor='none', edgecolor='black', linewidth=3.0)
                                   
            # Triangle 2 (pointing down)
            angles2 = np.array([270, 30, 150])
            rads2 = np.radians(angles2)
            x2 = cx + r * np.cos(rads2)
            y2 = cy + r * np.sin(rads2)
            
            poly2 = patches.Polygon(np.column_stack([x2, y2]), closed=True, 
                                   facecolor='none', edgecolor='black', linewidth=3.0)
                                   
            ax.add_patch(poly1)
            ax.add_patch(poly2)

    save(fig, "abstract grid tessellation triaxial kagome basket weave lattice pattern black white texture")


if __name__ == "__main__":
    draw()
