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
    Conway's Game of Life Cellular Automaton.
    A grid visualizing a late-stage snapshot of Conway's Game of Life,
    featuring gliders, blinkers, blocks, and organic cellular clusters.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.patches as patches

    grid_size = 50
    cell_size = 120.0 / grid_size
    
    # Initialize random grid
    state = rng.choice([0, 1], size=(grid_size, grid_size), p=[0.75, 0.25])
    
    # Evolve the game of life for a few generations to get organic clusters
    # rather than just static noise.
    
    for _ in range(15):
        new_state = np.copy(state)
        for r in range(grid_size):
            for c in range(grid_size):
                # Count neighbors
                neighbors = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr = (r + dr) % grid_size
                        nc = (c + dc) % grid_size
                        neighbors += state[nr, nc]
                        
                # Rules
                if state[r, c] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_state[r, c] = 0
                else:
                    if neighbors == 3:
                        new_state[r, c] = 1
        state = new_state

    # Draw the grid cells
    for r in range(grid_size):
        for c in range(grid_size):
            x = -10 + c * cell_size
            y = -10 + r * cell_size
            
            # Draw empty grid cell boundaries for texture
            rect_empty = patches.Rectangle((x, y), cell_size, cell_size, 
                                           linewidth=0.5, edgecolor='black', facecolor='none')
            ax.add_patch(rect_empty)
            
            if state[r, c] == 1:
                # Draw filled cell with a small margin
                margin = cell_size * 0.1
                rect_filled = patches.Rectangle((x + margin, y + margin), 
                                                cell_size - 2*margin, cell_size - 2*margin, 
                                                linewidth=0, facecolor='black')
                ax.add_patch(rect_filled)

    save(fig, "abstract grid tessellation conway game of life cellular automaton pattern black white texture")


if __name__ == "__main__":
    draw()
