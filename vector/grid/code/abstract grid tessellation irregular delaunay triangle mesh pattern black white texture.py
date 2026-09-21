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
    Irregular Delaunay Triangle Mesh.
    A grid made of random points connected into a dense, irregular
    triangle mesh, mimicking a low-poly 3D surface or cracked glass.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    from scipy.spatial import Delaunay
    import matplotlib.collections as collections

    # Generate somewhat clustered random points
    n_pts = 400
    points = rng.uniform(-15, 115, (n_pts, 2))
    
    # Add a dense cluster in the center to make it look like an impact
    cluster = rng.normal(50, 10, (100, 2))
    points = np.vstack([points, cluster])
    
    # Add boundary points to prevent edge artifacts
    boundary = []
    for x in np.linspace(-20, 120, 10):
        boundary.append([x, -20])
        boundary.append([x, 120])
        boundary.append([-20, x])
        boundary.append([120, x])
    points = np.vstack([points, boundary])

    tri = Delaunay(points)
    
    segments = []
    # Extract the edges from the simplices (triangles)
    for simplex in tri.simplices:
        p1 = points[simplex[0]]
        p2 = points[simplex[1]]
        p3 = points[simplex[2]]
        
        # Only add segments inside the viewport
        if (-10 <= p1[0] <= 110 and -10 <= p1[1] <= 110) or \
           (-10 <= p2[0] <= 110 and -10 <= p2[1] <= 110) or \
           (-10 <= p3[0] <= 110 and -10 <= p3[1] <= 110):
            segments.append([p1, p2])
            segments.append([p2, p3])
            segments.append([p3, p1])

    # collections handles duplicate segments efficiently
    lc = collections.LineCollection(segments, linewidths=1.0, colors="black")
    ax.add_collection(lc)
    
    # Draw tiny vertices
    ax.scatter(points[:, 0], points[:, 1], s=3, color="black", zorder=3)

    save(fig, "abstract grid tessellation irregular delaunay triangle mesh pattern black white texture")


if __name__ == "__main__":
    draw()
