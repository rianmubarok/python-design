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
    Interlocking Arrow Tessellation (Escher style).
    A seamless 2D tessellation using interlocking arrow shapes,
    shaded alternately to highlight the positive and negative space.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches

    scale = 8.0
    cols = int(120 / scale) + 2
    rows = int(120 / scale) + 2
    
    # An arrow that perfectly tessellates with itself.
    # Let's construct the polygon coordinates for a right-pointing arrow.
    # Centered roughly at origin.
    arrow = np.array([
        [-0.5, 0.25],  # Top left of tail
        [0.0, 0.25],   # Inner corner
        [0.0, 0.5],    # Top point of head
        [0.5, 0.0],    # Right tip
        [0.0, -0.5],   # Bottom point of head
        [0.0, -0.25],  # Inner corner
        [-0.5, -0.25], # Bottom left of tail
        [-0.25, 0.0]   # Indent in tail (matches the tip)
    ]) * scale
    
    # The tessellation works by shifting the arrow horizontally and vertically.
    # Because of the tail indent (-0.25) and tip (+0.5), horizontal shift is 0.75 * scale.
    # Vertical shift is 0.5 * scale (height of the tail/body).
    
    dx = 0.75 * scale
    dy = 0.5 * scale
    
    for row in range(-10, rows * 2):
        for col in range(-2, cols + 2):
            cx = col * dx
            cy = row * dy
            
            # The arrows must lock together.
            # In a standard arrow tessellation, alternating rows face opposite directions
            # OR they all face the same way and just slide in.
            # The geometry defined above slides in perfectly horizontally.
            # Vertically, the tail (width 0.5) perfectly stacks.
            
            # Add some alternating patterns for visual interest (Op-Art style)
            if (row + col) % 2 == 0:
                face = 'black'
                edge = 'none'
            else:
                face = 'white'
                edge = 'black'
                
            poly = patches.Polygon(arrow + [cx, cy], closed=True, 
                                  facecolor=face, edgecolor=edge, linewidth=1.5, joinstyle='miter')
            ax.add_patch(poly)

    save(fig, "abstract grid tessellation interlocking arrow directional tessellation pattern black white texture")


if __name__ == "__main__":
    draw()
