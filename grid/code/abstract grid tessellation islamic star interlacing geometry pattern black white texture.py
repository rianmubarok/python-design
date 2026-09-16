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
    Islamic Star Interlacing Geometry.
    A classic 8-point geometric star pattern (Khatam style) built by 
    rotating and overlapping squares, tiling endlessly.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches

    scale = 12.0
    cols = int(120 / scale) + 1
    rows = int(120 / scale) + 1
    
    # We can create an 8-point star (Khatam) by overlaying two squares, 
    # one rotated 45 degrees, and scaling them carefully.
    
    for row in range(-1, rows + 1):
        for col in range(-1, cols + 1):
            cx = col * scale
            cy = row * scale
            
            # The pattern looks best when adjacent cells alternate their rotations
            # or when we draw a complex set of intersecting lines across the grid.
            # A simpler way to get the true Islamic tessellation look:
            
            # Draw Square 1 (0 deg)
            s1 = patches.Rectangle((cx - scale/3, cy - scale/3), scale*(2/3), scale*(2/3), 
                                   angle=0, facecolor='none', edgecolor='black', linewidth=1.5)
            # Center of rotation for Rectangle is its bottom left corner by default, 
            # so we must rotate it manually or use Polygon.
            
            # Let's use polygons for precise centering
            r = scale * 0.4
            
            # Square 1
            sq1_angles = np.array([45, 135, 225, 315])
            sq1_rads = np.radians(sq1_angles)
            sq1_x = cx + r * np.cos(sq1_rads)
            sq1_y = cy + r * np.sin(sq1_rads)
            p1 = patches.Polygon(np.column_stack([sq1_x, sq1_y]), closed=True, 
                                 facecolor='none', edgecolor='black', linewidth=1.5)
                                 
            # Square 2 (rotated 45 degrees relative to Square 1)
            sq2_angles = np.array([0, 90, 180, 270])
            sq2_rads = np.radians(sq2_angles)
            sq2_x = cx + r * np.cos(sq2_rads)
            sq2_y = cy + r * np.sin(sq2_rads)
            p2 = patches.Polygon(np.column_stack([sq2_x, sq2_y]), closed=True, 
                                 facecolor='none', edgecolor='black', linewidth=1.5)
            
            ax.add_patch(p1)
            ax.add_patch(p2)
            
            # Draw connecting lines between stars to form the interlacing bands
            # The tips of Square 2 (0, 90, 180, 270) touch the adjacent cells
            # We also add a smaller inner 8-point star
            inner_r = r * 0.4
            sq1_inner_x = cx + inner_r * np.cos(sq1_rads)
            sq1_inner_y = cy + inner_r * np.sin(sq1_rads)
            p1_inner = patches.Polygon(np.column_stack([sq1_inner_x, sq1_inner_y]), closed=True, 
                                 facecolor='black', edgecolor='none')
            
            sq2_inner_x = cx + inner_r * np.cos(sq2_rads)
            sq2_inner_y = cy + inner_r * np.sin(sq2_rads)
            p2_inner = patches.Polygon(np.column_stack([sq2_inner_x, sq2_inner_y]), closed=True, 
                                 facecolor='black', edgecolor='none')
                                 
            ax.add_patch(p1_inner)
            ax.add_patch(p2_inner)

    # Adding diagonal connecting lines over the whole grid
    for i in range(-rows*2, rows*2):
        # / lines
        ax.plot([-10, 110], [i*scale - 10, i*scale + 110], color="black", linewidth=0.5, zorder=0)
        # \ lines
        ax.plot([-10, 110], [i*scale + 110, i*scale - 10], color="black", linewidth=0.5, zorder=0)

    save(fig, "abstract grid tessellation islamic star interlacing geometry pattern black white texture")


if __name__ == "__main__":
    draw()
