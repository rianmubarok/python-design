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
    Optical Illusion Spinning Pinwheel.
    A rigid grid where alternating triangles are shaded in a specific pattern
    to create a dizzying optical illusion that makes the grid look curved or spinning.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches

    grid_size = 20
    cell_size = 120.0 / grid_size
    
    # We create a Fraser spiral or Cafe Wall style illusion by drawing specifically
    # oriented triangles inside a grid.
    
    for row in range(-1, grid_size + 1):
        for col in range(-1, grid_size + 1):
            cx = -10 + col * cell_size
            cy = -10 + row * cell_size
            
            # Divide each cell into 4 triangles
            center_x = cx + cell_size / 2
            center_y = cy + cell_size / 2
            
            tl = [cx, cy + cell_size]
            tr = [cx + cell_size, cy + cell_size]
            bl = [cx, cy]
            br = [cx + cell_size, cy]
            c = [center_x, center_y]
            
            # The shading alternates based on a checkboard pattern to create
            # the spinning pinwheel illusion.
            # Pinwheel orientation depends on (row + col) % 2
            
            if (row + col) % 2 == 0:
                # Black on Top and Bottom
                poly_t = patches.Polygon([tl, tr, c], closed=True, facecolor='black', edgecolor='black')
                poly_b = patches.Polygon([br, bl, c], closed=True, facecolor='black', edgecolor='black')
                poly_l = patches.Polygon([bl, tl, c], closed=True, facecolor='white', edgecolor='black')
                poly_r = patches.Polygon([tr, br, c], closed=True, facecolor='white', edgecolor='black')
            else:
                # Black on Left and Right
                poly_t = patches.Polygon([tl, tr, c], closed=True, facecolor='white', edgecolor='black')
                poly_b = patches.Polygon([br, bl, c], closed=True, facecolor='white', edgecolor='black')
                poly_l = patches.Polygon([bl, tl, c], closed=True, facecolor='black', edgecolor='black')
                poly_r = patches.Polygon([tr, br, c], closed=True, facecolor='black', edgecolor='black')
                
            ax.add_patch(poly_t)
            ax.add_patch(poly_b)
            ax.add_patch(poly_l)
            ax.add_patch(poly_r)
            
            # Add a small offset white/black diamond in the center to amplify the illusion
            s = cell_size * 0.25
            dia_color = 'white' if (row + col) % 2 == 0 else 'black'
            dia_edge = 'black' if dia_color == 'white' else 'none'
            
            diamond = patches.Polygon([
                [center_x, center_y + s],
                [center_x + s, center_y],
                [center_x, center_y - s],
                [center_x - s, center_y]
            ], closed=True, facecolor=dia_color, edgecolor=dia_edge, linewidth=1.0)
            
            ax.add_patch(diamond)

    save(fig, "abstract grid tessellation optical illusion spinning pinwheel pattern black white texture")


if __name__ == "__main__":
    draw()
