import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from matplotlib.collections import LineCollection

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
    Magnetic Domain Wall / Hexagonal Honeycomb Lattice.
    Parallel lines deform around a honeycomb grid of cells.
    Lines passing near the center of a hexagon are compressed, 
    while those near the edges bend around the cell walls.
    """
    fig, ax = setup_ax()

    n_lines = 110
    n_pts = 600

    hex_size = 8.0
    # Create hex grid centers
    centers = []
    for row in range(-2, 16):
        for col in range(-2, 16):
            cx = col * hex_size * 1.5
            cy = row * hex_size * np.sqrt(3)
            if col % 2 == 1:
                cy += hex_size * np.sqrt(3) / 2
            centers.append((cx, cy))

    centers = np.array(centers)

    for i in range(n_lines):
        y0 = -5 + 110 * i / (n_lines - 1)
        x = np.linspace(-5, 105, n_pts)
        
        y_warped = np.full(n_pts, y0)
        
        for j in range(n_pts):
            px, py = x[j], y_warped[j]
            # Find closest hex center
            dists = (centers[:, 0] - px)**2 + (centers[:, 1] - py)**2
            idx = np.argmin(dists)
            cx, cy = centers[idx]
            
            dx = px - cx
            dy = py - cy
            dist = np.sqrt(dx**2 + dy**2)
            
            if dist < hex_size:
                # Push points toward the edges of the hexagon
                # Creates a domain wall effect where lines bunch up at cell boundaries
                push = (hex_size - dist) * 0.4
                if dist > 0.1:
                    y_warped[j] += (dy / dist) * push
                    
        # Smooth out the sharp transitions
        window = np.ones(5) / 5.0
        y_smooth = np.convolve(y_warped, window, mode='same')
        # Fix boundary artifacts of convolution
        y_smooth[:3] = y_warped[:3]
        y_smooth[-3:] = y_warped[-3:]

        ax.plot(x, y_smooth, color="black", linewidth=0.4, solid_capstyle="round")

    save(fig, "abstract parallel lines hexagonal honeycomb lattice pattern black white texture")


if __name__ == "__main__":
    draw()
