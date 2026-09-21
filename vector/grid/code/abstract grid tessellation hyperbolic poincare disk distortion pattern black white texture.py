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
    Hyperbolic Poincare Disk Distortion.
    A regular grid distorted mathematically to fit into a Poincare disk model
    of hyperbolic geometry, where cells get infinitely smaller at the edges.
    """
    fig, ax = setup_ax()

    # Draw the boundary circle
    import matplotlib.patches as patches
    disk = patches.Circle((50, 50), 50, facecolor='none', edgecolor='black', linewidth=3)
    ax.add_patch(disk)

    # We will generate a Cartesian grid and map it to the disk
    # The mapping from complex plane (x + iy) to Poincare disk is a Mobius transformation.
    # However, a simpler visual approximation is compressing distance r -> tanh(r).
    # Let's map an infinite plane onto a unit circle via r_new = 2/pi * arctan(r)
    
    n_lines = 40
    
    def map_to_disk(x, y):
        # Center at 0,0
        cx = (x - 50) / 10.0
        cy = (y - 50) / 10.0
        
        r = np.sqrt(cx**2 + cy**2)
        theta = np.arctan2(cy, cx)
        
        # Compress r to [0, 1) using a sigmoid-like function
        r_new = (2 / np.pi) * np.arctan(r * 0.3)
        
        # Scale back to 50 radius
        x_new = 50 + 50 * r_new * np.cos(theta)
        y_new = 50 + 50 * r_new * np.sin(theta)
        return x_new, y_new

    # Vertical lines mapped
    for i in range(-n_lines, n_lines + 1):
        x = np.full(500, 50 + i * 5)
        y = np.linspace(-500, 600, 500)
        
        mx, my = map_to_disk(x, y)
        ax.plot(mx, my, color="black", linewidth=1.0)
        
    # Horizontal lines mapped
    for i in range(-n_lines, n_lines + 1):
        y = np.full(500, 50 + i * 5)
        x = np.linspace(-500, 600, 500)
        
        mx, my = map_to_disk(x, y)
        ax.plot(mx, my, color="black", linewidth=1.0)

    save(fig, "abstract grid tessellation hyperbolic poincare disk distortion pattern black white texture")


if __name__ == "__main__":
    draw()
