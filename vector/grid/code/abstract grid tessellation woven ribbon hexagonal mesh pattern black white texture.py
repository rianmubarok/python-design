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
    Woven Ribbon Hexagonal Mesh.
    A hexagonal grid where the edges are thick woven ribbons that overlap
    each other, simulating a complex basket weave or carbon structure.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches

    scale = 8.0
    h = scale * np.sqrt(3) / 2.0
    
    cols = int(120 / (scale * 1.5)) + 2
    rows = int(120 / h) + 2
    
    # A standard hex grid
    # To create a weave effect, the edges of the hexagon must be drawn as thick lines
    # that overlap. An easy way to achieve this is to draw the edges as individual line
    # segments in a specific order, using white outlines to cut overlapping lines.
    
    import matplotlib.collections as collections
    
    # We collect 3 types of edges based on their angle: 30, 90, 150 degrees
    # By plotting all edges of angle 30, then 90, then 150, we naturally create an overlap.
    # To make it a true weave (over, under, over), we'd need more complex z-sorting.
    # Layering by angle gives a pseudo-weave that looks like stacked 3D layers.
    
    edges_30 = []
    edges_90 = []
    edges_150 = []
    
    for row in range(-2, rows):
        for col in range(-2, cols):
            cx = col * scale * 1.5
            cy = row * h * 2.0
            if col % 2 != 0:
                cy += h
                
            # Hexagon vertices
            hex_pts = []
            for angle in range(0, 360, 60):
                rad = np.radians(angle)
                hex_pts.append((cx + scale * np.cos(rad), cy + scale * np.sin(rad)))
                
            # The edges are (0,1), (1,2), (2,3), (3,4), (4,5), (5,0)
            # Edge angles are approx 120, 180, 240, 300, 0, 60
            # We group them into 3 parallel sets.
            # 60 and 240 -> parallel (edges_150 / 60)
            # 120 and 300 -> parallel (edges_30 / 120)
            # 0 and 180 -> parallel (edges_90 / 0)
            
            # To avoid drawing duplicates, we could use a set, but collections handles overlap fine
            edges_90.append([hex_pts[1], hex_pts[2]])
            edges_90.append([hex_pts[4], hex_pts[5]])
            
            edges_150.append([hex_pts[2], hex_pts[3]])
            edges_150.append([hex_pts[5], hex_pts[0]])
            
            edges_30.append([hex_pts[3], hex_pts[4]])
            edges_30.append([hex_pts[0], hex_pts[1]])
            
    # Draw them in layers, thick black with white cutout
    def draw_layer(edges):
        # White cutout
        ax.add_collection(collections.LineCollection(edges, linewidths=12.0, colors="white", capstyle="round"))
        # Black fill
        ax.add_collection(collections.LineCollection(edges, linewidths=8.0, colors="black", capstyle="round"))
        # Inner white line for texture
        ax.add_collection(collections.LineCollection(edges, linewidths=1.5, colors="white", capstyle="round"))

    # Layering creates the overlap illusion
    draw_layer(edges_30)
    draw_layer(edges_90)
    draw_layer(edges_150)

    save(fig, "abstract grid tessellation woven ribbon hexagonal mesh pattern black white texture")


if __name__ == "__main__":
    draw()
