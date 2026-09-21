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
    Cairo Pentagonal Tiling.
    A traditional geometric tessellation using 5-sided polygons (pentagons),
    arranged in interlocking baskets.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches
    
    # A Cairo pentagon can be formed by bisecting a hexagon or joining squares.
    # We will construct the tiling mathematically.
    # The standard Cairo tiling has vertices at integer coordinates (even, even)
    # and midpoints of segments connecting them.
    # A simpler way is to map standard tiles.
    
    scale = 3.5
    cols = 20
    rows = 20
    
    # Define a single Cairo pentagon base centered near origin, pointing right
    # (x, y) coordinates
    p_base = np.array([
        [0, scale],
        [scale*1.4, scale*1.4],
        [scale, 0],
        [scale*1.4, -scale*1.4],
        [0, -scale]
    ])

    # The Cairo tiling consists of two orientations of pentagons.
    # We can tile it by placing 4 pentagons around every alternating grid node.
    
    # Center the grid on (50, 50)
    grid_cx = 50.0
    grid_cy = 50.0
    
    for row in range(-rows // 2 - 2, rows // 2 + 3):
        for col in range(-cols // 2 - 2, cols // 2 + 3):
            cx = grid_cx + col * scale * 2.0
            cy = grid_cy + row * scale * 2.0
            
            # The tiling alternates
            if (row + col) % 2 == 0:
                # Node type A: 4 pentagons radiating outward
                for angle in [0, 90, 180, 270]:
                    rad = np.radians(angle)
                    rot_matrix = np.array([[np.cos(rad), -np.sin(rad)], 
                                           [np.sin(rad), np.cos(rad)]])
                    
                    rotated_p = np.dot(p_base, rot_matrix.T)
                    
                    # Shift to node
                    poly = patches.Polygon(rotated_p + [cx, cy], closed=True, 
                                          facecolor='none', edgecolor='black', linewidth=1.5)
                    ax.add_patch(poly)
                    
                    # Add inner concentric pentagon for texture
                    inner_p = rotated_p * 0.7
                    inner_poly = patches.Polygon(inner_p + [cx, cy], closed=True, 
                                          facecolor='none', edgecolor='black', linewidth=0.5)
                    ax.add_patch(inner_poly)
                    
                    # Add center dot
                    ax.scatter([cx], [cy], s=4.0, color='black')

    save(fig, "abstract grid tessellation cairo pentagonal tiling pattern black white texture")


if __name__ == "__main__":
    draw()
