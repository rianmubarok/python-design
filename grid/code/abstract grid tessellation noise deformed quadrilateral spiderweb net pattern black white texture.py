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
    Noise Deformed Quadrilateral Spiderweb Net.
    A standard square grid where every vertex is displaced randomly by noise,
    creating a wobbly spiderweb net of quadrilaterals.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.collections as collections

    grid_size = 25
    spacing = 140.0 / grid_size
    
    # Generate points
    pts = np.zeros((grid_size, grid_size, 2))
    for r in range(grid_size):
        for c in range(grid_size):
            base_x = -20 + c * spacing
            base_y = -20 + r * spacing
            
            # Displacement
            dist_to_center = np.sqrt((base_x - 50)**2 + (base_y - 50)**2)
            
            # More distortion in the center
            mag = max(0, (60 - dist_to_center) * 0.15)
            
            dx = rng.uniform(-mag, mag)
            dy = rng.uniform(-mag, mag)
            
            pts[r, c] = [base_x + dx, base_y + dy]
            
    segments = []
    
    # Horizontal lines
    for r in range(grid_size):
        for c in range(grid_size - 1):
            segments.append([pts[r, c], pts[r, c+1]])
            
    # Vertical lines
    for c in range(grid_size):
        for r in range(grid_size - 1):
            segments.append([pts[r, c], pts[r+1, c]])
            
    # Diagonal lines (add to make it look like a structural net)
    for r in range(grid_size - 1):
        for c in range(grid_size - 1):
            if rng.random() > 0.5:
                segments.append([pts[r, c], pts[r+1, c+1]])
            else:
                segments.append([pts[r+1, c], pts[r, c+1]])

    # Variable line width based on strain (distance between points)
    linewidths = []
    for p1, p2 in segments:
        dist = np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        # Shorter lines = thicker (bunched up), longer lines = thinner (stretched)
        lw = np.clip(10.0 / max(dist, 1.0), 0.2, 4.0)
        linewidths.append(lw)

    lc = collections.LineCollection(segments, linewidths=linewidths, colors="black", capstyle="round")
    ax.add_collection(lc)

    save(fig, "abstract grid tessellation noise deformed quadrilateral spiderweb net pattern black white texture")


if __name__ == "__main__":
    draw()
