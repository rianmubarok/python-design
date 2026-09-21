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
    Hexagonal Voronoi Bubble Foam.
    A relaxed Voronoi diagram (Lloyd's algorithm approximation) to create
    a natural, organic bubble foam or distorted honeycomb.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    from scipy.spatial import Voronoi
    import matplotlib.collections as collections

    n_points = 250
    points = rng.uniform(-20, 120, (n_points, 2))
    
    # Lloyd's algorithm approximation (relax the points by moving them to the centroid of their Voronoi cells)
    # We will do 3 iterations for a natural foam look (not perfectly hexagonal, but relaxed)
    
    for _ in range(3):
        vor = Voronoi(points)
        centroids = []
        for region_idx in vor.point_region:
            region = vor.regions[region_idx]
            if not region or -1 in region:
                # Infinite region, just keep the point
                centroids.append(points[np.where(vor.point_region == region_idx)[0][0]])
            else:
                polygon = [vor.vertices[i] for i in region]
                # Calculate centroid of polygon
                x_sum = sum([p[0] for p in polygon])
                y_sum = sum([p[1] for p in polygon])
                centroids.append([x_sum / len(polygon), y_sum / len(polygon)])
        points = np.array(centroids)
        
    # Final Voronoi
    vor = Voronoi(points)
    
    segments = []
    for simplex in vor.ridge_vertices:
        if -1 not in simplex:
            p1 = vor.vertices[simplex[0]]
            p2 = vor.vertices[simplex[1]]
            # Only add segments near viewport
            if (-10 <= p1[0] <= 110 and -10 <= p1[1] <= 110) or (-10 <= p2[0] <= 110 and -10 <= p2[1] <= 110):
                segments.append([p1, p2])

    # To make it look like organic foam, we use thick rounded lines
    # and maybe some tiny bubbles (circles) in the vertices.
    lc = collections.LineCollection(segments, linewidths=rng.uniform(1.5, 4.0, len(segments)), 
                                    colors="black", capstyle="round", joinstyle="round")
    ax.add_collection(lc)
    
    # Add bubbles at the vertices for a liquid foam effect
    valid_vertices = [p for p in vor.vertices if -10 <= p[0] <= 110 and -10 <= p[1] <= 110]
    vertices_x = [p[0] for p in valid_vertices]
    vertices_y = [p[1] for p in valid_vertices]
    
    import matplotlib.patches as patches
    for vx, vy in zip(vertices_x, vertices_y):
        r = rng.uniform(0.5, 2.5)
        c = patches.Circle((vx, vy), r, facecolor='white', edgecolor='black', linewidth=1.5, zorder=3)
        ax.add_patch(c)
        
        # Add a tiny highlight dot to the bubble
        dot = patches.Circle((vx + r*0.3, vy + r*0.3), r*0.15, facecolor='black', edgecolor='none', zorder=4)
        ax.add_patch(dot)

    save(fig, "abstract grid tessellation hexagonal voronoi bubble foam pattern black white texture")


if __name__ == "__main__":
    draw()
