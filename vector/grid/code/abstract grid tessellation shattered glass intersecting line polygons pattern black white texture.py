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
    Shattered Glass Intersecting Lines.
    A grid created purely by slicing the canvas with random straight lines,
    generating a chaotic, abstract polygon tessellation mimicking shattered glass.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    n_lines = 100
    
    # We define lines by two points far outside the viewport
    # A center point, and an angle
    centers_x = rng.uniform(-10, 110, n_lines)
    centers_y = rng.uniform(-10, 110, n_lines)
    angles = rng.uniform(0, np.pi, n_lines)
    
    # Some lines should originate from a "shatter point" to simulate an impact
    impact_x, impact_y = 40.0, 60.0
    impact_lines = 35
    for i in range(impact_lines):
        centers_x[i] = impact_x
        centers_y[i] = impact_y
        # Add slight jitter to impact center so they don't perfectly overlap
        centers_x[i] += rng.normal(0, 1.5)
        centers_y[i] += rng.normal(0, 1.5)
        angles[i] = i * (np.pi / impact_lines) + rng.uniform(-0.05, 0.05)

    import matplotlib.collections as collections
    
    segments = []
    linewidths = []
    
    for cx, cy, angle in zip(centers_x, centers_y, angles):
        length = 200.0
        
        x1 = cx - np.cos(angle) * length
        y1 = cy - np.sin(angle) * length
        x2 = cx + np.cos(angle) * length
        y2 = cy + np.sin(angle) * length
        
        segments.append([(x1, y1), (x2, y2)])
        
        # Thicker lines near the impact, thinner elsewhere
        dist_to_impact = np.sqrt((cx - impact_x)**2 + (cy - impact_y)**2)
        if dist_to_impact < 5.0:
            linewidths.append(rng.uniform(1.5, 3.5))
        else:
            linewidths.append(rng.uniform(0.2, 1.2))
            
    lc = collections.LineCollection(segments, linewidths=linewidths, colors="black")
    ax.add_collection(lc)
    
    # Draw some solid black shards randomly (for texture)
    # We can do this by just filling in random triangles between the shatter points
    from scipy.spatial import Delaunay
    
    # Use the line centers for a quick delaunay triangulation to fill some shapes
    points = np.column_stack((centers_x, centers_y))
    tri = Delaunay(points)
    
    import matplotlib.patches as patches
    
    for simplex in tri.simplices:
        if rng.random() > 0.95:
            p1 = points[simplex[0]]
            p2 = points[simplex[1]]
            p3 = points[simplex[2]]
            
            # Don't draw huge triangles
            area = 0.5 * np.abs(p1[0]*(p2[1]-p3[1]) + p2[0]*(p3[1]-p1[1]) + p3[0]*(p1[1]-p2[1]))
            if area < 50.0:
                poly = patches.Polygon([p1, p2, p3], closed=True, facecolor='black', edgecolor='none')
                ax.add_patch(poly)

    save(fig, "abstract grid tessellation shattered glass intersecting line polygons pattern black white texture")


if __name__ == "__main__":
    draw()
