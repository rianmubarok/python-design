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
    Hexagonal Honeycomb Lattice.
    A rigid geometric honeycomb grid with varying border thicknesses
    to simulate a lighting or gradient effect across the tessellation.
    """
    fig, ax = setup_ax()

    hex_size = 3.5
    h = hex_size * np.sqrt(3) / 2.0
    
    cols = int(120 / (hex_size * 1.5)) + 2
    rows = int(120 / h) + 2

    import matplotlib.patches as patches
    
    # Center of lighting gradient
    lx, ly = 80.0, 80.0

    for row in range(-2, rows):
        for col in range(-2, cols):
            cx = col * hex_size * 1.5
            cy = row * h * 2.0
            if col % 2 != 0:
                cy += h
                
            # Create a regular hexagon
            angles = np.linspace(0, 2*np.pi, 7)
            hx = cx + hex_size * np.cos(angles)
            hy = cy + hex_size * np.sin(angles)
            
            # Gradient thickness based on distance to (lx, ly)
            dist = np.sqrt((cx - lx)**2 + (cy - ly)**2)
            lw = max(0.2, 5.0 - dist / 25.0)
            
            # Draw individual hexagon borders
            ax.plot(hx, hy, color="black", linewidth=lw, solid_joinstyle="miter")

    save(fig, "abstract grid tessellation hexagonal honeycomb pattern black white texture")


if __name__ == "__main__":
    draw()
