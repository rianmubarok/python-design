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
    3D Isometric Cityscape Skyscrapers.
    A dense grid of isometric buildings of varying heights, creating
    the illusion of a sprawling, abstract megacity.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.patches as patches

    # Grid coordinates
    cols = 20
    rows = 20
    
    cube_size = 4.5
    h = cube_size * np.sqrt(3) / 2.0
    
    # Face definitions relative to bottom-center of the prism
    # Given a height H, the building is drawn by extending the isometric sides up.
    
    def draw_building(cx, cy, height):
        # We need to draw 3 faces: Top, Left, Right
        
        # Base points for the isometric hexagon (width = 2*cube_size)
        p1_base = np.array([0, 0]) # Bottom center
        p2_base = np.array([cube_size * np.cos(np.pi/6), cube_size * np.sin(np.pi/6)]) # Right mid
        p3_base = np.array([0, 2 * cube_size * np.sin(np.pi/6)]) # Top center (if height=0)
        p4_base = np.array([-cube_size * np.cos(np.pi/6), cube_size * np.sin(np.pi/6)]) # Left mid
        
        # Shift everything up by height
        p1_top = p1_base + np.array([0, height])
        p2_top = p2_base + np.array([0, height])
        p3_top = p3_base + np.array([0, height])
        p4_top = p4_base + np.array([0, height])
        
        # Top Face
        face_top = [p1_top, p2_top, p3_top, p4_top]
        
        # Left Face
        face_left = [p1_base, p1_top, p4_top, p4_base]
        
        # Right Face
        face_right = [p1_base, p2_base, p2_top, p1_top]
        
        # Styles
        # Top is white, left is hatched, right is black
        
        poly_t = patches.Polygon(np.array(face_top) + [cx, cy], closed=True, 
                                 facecolor='white', edgecolor='black', linewidth=1.2)
        poly_l = patches.Polygon(np.array(face_left) + [cx, cy], closed=True, 
                                 facecolor='none', edgecolor='black', linewidth=1.2, hatch='///')
        poly_r = patches.Polygon(np.array(face_right) + [cx, cy], closed=True, 
                                 facecolor='black', edgecolor='black', linewidth=1.2)
                                 
        ax.add_patch(poly_t)
        ax.add_patch(poly_l)
        ax.add_patch(poly_r)
        
        # Draw some windows on the white Top face for tall buildings to simulate rooftops
        if height > 15:
            s = cube_size * 0.3
            ax.add_patch(patches.Rectangle((cx - s/2, cy + height + s/2), s, s, facecolor='black'))

    # Generate heights using a cluster map (Perlin-ish)
    heights = np.zeros((rows, cols))
    for r in range(rows):
        for c in range(cols):
            # Distance from center
            dist = np.sqrt((r - rows/2)**2 + (c - cols/2)**2)
            # Higher in the center, lower at edges, plus noise
            base_h = max(0, (15 - dist) * 2)
            noise = rng.uniform(0, 15)
            heights[r, c] = base_h + noise

    # Sort drawing order for isometric (back to front)
    # y determines depth. Top of screen is back.
    for row in reversed(range(-2, rows + 2)):
        for col in range(-2, cols + 2):
            cx = col * (cube_size * np.cos(np.pi/6) * 2)
            cy = row * h * 2
            
            # Stagger columns
            if row % 2 != 0:
                cx += cube_size * np.cos(np.pi/6)
                
            # Clamp array indices
            h_r = np.clip(row, 0, rows-1)
            h_c = np.clip(col, 0, cols-1)
            height = heights[h_r, h_c]
            
            draw_building(cx, cy - 20, height) # Shifted down to center

    save(fig, "abstract grid tessellation isometric 3d cityscape skyscrapers pattern black white texture")


if __name__ == "__main__":
    draw()
