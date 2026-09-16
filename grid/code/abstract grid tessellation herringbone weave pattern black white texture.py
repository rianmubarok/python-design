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
    Herringbone Weave Tessellation.
    An overlapping grid of rectangles arranged in a zig-zag herringbone
    pattern, with parallel internal lines to emphasize the fabric weave look.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches
    
    width = 3.0
    length = 12.0
    
    cols = 20
    rows = 20
    
    for row in range(-5, rows + 5):
        for col in range(-5, cols + 5):
            # Alternating slant
            if col % 2 == 0:
                cx = col * (width + length/np.sqrt(2)) * 0.5
                cy = row * (width + length/np.sqrt(2))
                angle = 45.0
            else:
                cx = col * (width + length/np.sqrt(2)) * 0.5
                cy = row * (width + length/np.sqrt(2)) + (width + length/np.sqrt(2)) * 0.5
                angle = -45.0
                
            # Draw the boundary of the rectangular weave segment
            rect = patches.Rectangle((0, 0), length, width, angle=angle,
                                   linewidth=1.0, edgecolor='black', facecolor='white')
                                   
            # We need to shift it so the center of the rectangle is at (cx, cy)
            # Center offset
            dx = (length * np.cos(np.radians(angle)) - width * np.sin(np.radians(angle))) / 2
            dy = (length * np.sin(np.radians(angle)) + width * np.cos(np.radians(angle))) / 2
            
            rect.set_xy((cx - dx, cy - dy))
            
            # Draw parallel fill lines inside the rectangle
            ax.add_patch(rect)
            
            # Instead of standard fill, we manually draw the parallel lines inside
            # for a true abstract pattern look.
            n_lines = 4
            for i in range(1, n_lines):
                # Offset along the width
                offset_w = width * (i / n_lines)
                
                # Base points at (0, offset_w) and (length, offset_w)
                px1 = 0
                py1 = offset_w
                px2 = length
                py2 = offset_w
                
                # Rotate and translate
                rad = np.radians(angle)
                rx1 = px1 * np.cos(rad) - py1 * np.sin(rad) + (cx - dx)
                ry1 = px1 * np.sin(rad) + py1 * np.cos(rad) + (cy - dy)
                
                rx2 = px2 * np.cos(rad) - py2 * np.sin(rad) + (cx - dx)
                ry2 = px2 * np.sin(rad) + py2 * np.cos(rad) + (cy - dy)
                
                ax.plot([rx1, rx2], [ry1, ry2], color="black", linewidth=0.5, zorder=2)

    save(fig, "abstract grid tessellation herringbone weave pattern black white texture")


if __name__ == "__main__":
    draw()
