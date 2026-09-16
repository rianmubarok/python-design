import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import sys

# Increase recursion depth for maze generation
sys.setrecursionlimit(5000)

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
    Orthogonal Labyrinth Maze.
    A continuous maze generated on a square grid using randomized depth-first search.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.collections as collections

    cols = 40
    rows = 40
    cell_size = 120.0 / cols

    # Maze generation data structures
    # Array of [Top, Right, Bottom, Left] walls
    maze = np.ones((rows, cols, 4), dtype=bool)
    visited = np.zeros((rows, cols), dtype=bool)

    # Directions: (dx, dy, wall_to_knock, opposite_wall)
    # Note: row is y, col is x.
    # Top is -1 row (index 0), Bottom is +1 row (index 2)
    # Right is +1 col (index 1), Left is -1 col (index 3)
    directions = [
        (0, -1, 0, 2),  # Top
        (1, 0, 1, 3),   # Right
        (0, 1, 2, 0),   # Bottom
        (-1, 0, 3, 1)   # Left
    ]

    def carve(cx, cy):
        visited[cy, cx] = True
        
        # Shuffle directions for random paths
        dirs = list(directions)
        rng.shuffle(dirs)
        
        for dx, dy, wall, opp_wall in dirs:
            nx, ny = cx + dx, cy + dy
            
            if 0 <= nx < cols and 0 <= ny < rows and not visited[ny, nx]:
                # Knock down walls
                maze[cy, cx, wall] = False
                maze[ny, nx, opp_wall] = False
                carve(nx, ny)

    # Start generation from center
    carve(cols // 2, rows // 2)

    # Draw the maze
    segments = []
    
    for r in range(rows):
        for c in range(cols):
            x = -10 + c * cell_size
            y = 110 - r * cell_size  # Invert y so row 0 is top
            
            if maze[r, c, 0]: # Top
                segments.append([(x, y), (x + cell_size, y)])
            if maze[r, c, 1]: # Right
                segments.append([(x + cell_size, y), (x + cell_size, y - cell_size)])
            if maze[r, c, 2]: # Bottom
                segments.append([(x, y - cell_size), (x + cell_size, y - cell_size)])
            if maze[r, c, 3]: # Left
                segments.append([(x, y), (x, y - cell_size)])

    lc = collections.LineCollection(segments, linewidths=2.5, colors="black", capstyle="round")
    ax.add_collection(lc)

    save(fig, "abstract grid tessellation orthogonal labyrinth maze generation pattern black white texture")


if __name__ == "__main__":
    draw()
