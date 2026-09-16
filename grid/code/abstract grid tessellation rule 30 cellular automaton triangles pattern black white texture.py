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
    Rule 30 Cellular Automaton Triangles.
    A grid visualizing the famous 1D cellular automaton Rule 30, which generates
    complex, chaotic Sierpinski-like triangle patterns.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches

    grid_size = 80
    cell_size = 120.0 / grid_size
    
    # Rule 30 logic
    # Maps local neighborhood [L, C, R] to new center state
    # 111 -> 0, 110 -> 0, 101 -> 0, 100 -> 1, 011 -> 1, 010 -> 1, 001 -> 1, 000 -> 0
    rule = {
        (1, 1, 1): 0,
        (1, 1, 0): 0,
        (1, 0, 1): 0,
        (1, 0, 0): 1,
        (0, 1, 1): 1,
        (0, 1, 0): 1,
        (0, 0, 1): 1,
        (0, 0, 0): 0,
    }
    
    # We need a wider array to prevent edge wrap-around artifacts
    width = grid_size * 2
    state = np.zeros((grid_size, width), dtype=int)
    
    # Initial condition: a single active cell in the center
    state[0, width // 2] = 1
    
    # Evolve
    for r in range(1, grid_size):
        for c in range(1, width - 1):
            L = state[r-1, c-1]
            C = state[r-1, c]
            R = state[r-1, c+1]
            state[r, c] = rule[(L, C, R)]

    # Draw the grid
    # We extract the center portion of the width
    start_c = (width - grid_size) // 2
    
    for r in range(grid_size):
        for c in range(grid_size):
            val = state[r, start_c + c]
            
            x = -10 + c * cell_size
            y = 110 - r * cell_size - cell_size # Top to bottom
            
            if val == 1:
                # Solid black block
                rect = patches.Rectangle((x, y), cell_size, cell_size, 
                                         linewidth=0, facecolor='black')
                ax.add_patch(rect)
            else:
                # Add a faint dot to white blocks for texture
                dot = patches.Circle((x + cell_size/2, y + cell_size/2), cell_size*0.1, color='black')
                ax.add_patch(dot)
                
            # Faint grid lines
            rect_empty = patches.Rectangle((x, y), cell_size, cell_size, 
                                           linewidth=0.1, edgecolor='black', facecolor='none')
            ax.add_patch(rect_empty)

    save(fig, "abstract grid tessellation rule 30 cellular automaton triangles pattern black white texture")


if __name__ == "__main__":
    draw()
