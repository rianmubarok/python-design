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
    Voronoi Cellular Tessellation.
    Generates an organic-looking cellular grid structure using Voronoi diagrams.
    The edges of the cells are drawn with varying thicknesses.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    # Scipy is usually available, if not this will throw an error and we can rewrite it
    from scipy.spatial import Voronoi

    # Generate random points
    points = rng.uniform(-10, 110, (150, 2))
    
    # Add boundary points to close the outer cells
    boundary = np.array([
        [-50, -50], [-50, 150], [150, -50], [150, 150],
        [50, -50], [50, 150], [-50, 50], [150, 50]
    ])
    points = np.vstack([points, boundary])

    vor = Voronoi(points)

    import matplotlib.collections as collections
    
    segments = []
    linewidths = []
    
    # Extract the line segments
    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            p1 = vor.vertices[simplex[0]]
            p2 = vor.vertices[simplex[1]]
            
            # Only include lines that are reasonably close to the viewport
            if -20 <= p1[0] <= 120 and -20 <= p1[1] <= 120:
                segments.append([p1, p2])
                # Randomize line thickness slightly for an organic look
                linewidths.append(rng.uniform(0.5, 3.5))

    lc = collections.LineCollection(segments, linewidths=linewidths, colors="black", capstyle="round")
    ax.add_collection(lc)
    
    # Draw tiny dots at the vertices
    valid_vertices = [p for p in vor.vertices if -10 <= p[0] <= 110 and -10 <= p[1] <= 110]
    vertices_x = [p[0] for p in valid_vertices]
    vertices_y = [p[1] for p in valid_vertices]
    ax.scatter(vertices_x, vertices_y, s=8, color="black", zorder=3)

    save(fig, "abstract grid tessellation voronoi cellular noise pattern black white texture")


if __name__ == "__main__":
    draw()
