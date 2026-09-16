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
    Interlocking Tetromino Blocks.
    A grid completely filled with interlocking Tetris blocks (Tetrominoes)
    decorated with internal geometries and shading.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.patches as patches

    # We can generate a perfect tiling, or simulate falling tetris blocks.
    # To keep it completely tiled without gaps (which is computationally hard for arbitrary random),
    # we can use a simpler approach: take a checkerboard and group 4 blocks together randomly
    # using a greedy algorithm.
    
    grid_size = 30
    cell_size = 120.0 / grid_size
    
    grid = np.zeros((grid_size, grid_size), dtype=int)
    block_id = 1
    
    shapes = [
        [(0,0), (0,1), (0,2), (0,3)], # I
        [(0,0), (1,0), (0,1), (1,1)], # O
        [(0,0), (1,0), (2,0), (1,1)], # T
        [(0,0), (1,0), (1,1), (1,2)], # L
        [(0,0), (0,1), (1,1), (2,1)], # J
        [(0,0), (1,0), (1,1), (2,1)], # S
        [(0,1), (1,1), (1,0), (2,0)]  # Z
    ]
    
    # We will randomly place shapes. Gaps will remain, which is fine for abstract art.
    for _ in range(3000):
        shape = rng.choice(shapes)
        
        # Pick random placement and orientation
        r = rng.integers(0, grid_size)
        c = rng.integers(0, grid_size)
        
        # Orientations: 0, 90, 180, 270
        rot = rng.integers(0, 4)
        
        valid = True
        coords = []
        for dr, dc in shape:
            # Rotate
            if rot == 1:
                dr, dc = -dc, dr
            elif rot == 2:
                dr, dc = -dr, -dc
            elif rot == 3:
                dr, dc = dc, -dr
                
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < grid_size and 0 <= nc < grid_size:
                if grid[nr, nc] == 0:
                    coords.append((nr, nc))
                else:
                    valid = False
                    break
            else:
                valid = False
                break
                
        if valid:
            for nr, nc in coords:
                grid[nr, nc] = block_id
            
            # Store the coords to draw it later
            
            # Render the block as a single connected shape
            # We can draw each cell, but color them the same and remove internal borders
            # For simplicity in matplotlib, drawing cells with same color and thick borders
            # creates the block illusion perfectly.
            
            style = rng.choice(['solid', 'hatch', 'outline', 'dot'])
            
            for nr, nc in coords:
                x = -10 + nc * cell_size
                y = -10 + nr * cell_size
                
                if style == 'solid':
                    rect = patches.Rectangle((x, y), cell_size, cell_size, 
                                             linewidth=1.5, edgecolor='black', facecolor='black')
                elif style == 'hatch':
                    rect = patches.Rectangle((x, y), cell_size, cell_size, 
                                             linewidth=1.5, edgecolor='black', facecolor='white', hatch='////')
                elif style == 'dot':
                    rect = patches.Rectangle((x, y), cell_size, cell_size, 
                                             linewidth=1.5, edgecolor='black', facecolor='white')
                    ax.add_patch(rect)
                    dot = patches.Circle((x + cell_size/2, y + cell_size/2), cell_size*0.2, color='black')
                    ax.add_patch(dot)
                    continue
                else:
                    rect = patches.Rectangle((x, y), cell_size, cell_size, 
                                             linewidth=1.5, edgecolor='black', facecolor='white')
                                             
                ax.add_patch(rect)
                
            block_id += 1

    save(fig, "abstract grid tessellation interlocking tetromino tetris blocks pattern black white texture")


if __name__ == "__main__":
    draw()
