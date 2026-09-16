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
    Printed Circuit Board Trace Routing.
    A grid of horizontal, vertical, and 45-degree traces connecting randomly
    placed square 'chips' and circular 'vias', simulating PCB routing.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.patches as patches

    grid_size = 25
    cell_size = 120.0 / grid_size
    
    # 0 = empty, 1 = node, 2 = trace
    grid = np.zeros((grid_size, grid_size), dtype=int)
    
    # Place nodes (chips/vias)
    nodes = []
    for _ in range(40):
        r = rng.integers(1, grid_size - 1)
        c = rng.integers(1, grid_size - 1)
        if grid[r, c] == 0:
            grid[r, c] = 1
            nodes.append((r, c))
            
    # Connect nodes using random walks constrained to 0, 90, 45 degree angles
    import matplotlib.collections as collections
    segments = []
    
    for i in range(len(nodes) - 1):
        r1, c1 = nodes[i]
        # Target a random node
        r2, c2 = rng.choice(nodes)
        
        if r1 == r2 and c1 == c2: continue
        
        # A simple routing that goes horizontally, then 45 deg, then vertically
        # Just drawing the lines (abstract representation, no perfect collision avoidance)
        
        x1 = -10 + c1 * cell_size
        y1 = -10 + r1 * cell_size
        x2 = -10 + c2 * cell_size
        y2 = -10 + r2 * cell_size
        
        # To make it look like a PCB, routes must snap to 45 deg angles.
        # Find the elbow point.
        dx = x2 - x1
        dy = y2 - y1
        
        # Move diagonally until one axis aligns
        dist_diag = min(abs(dx), abs(dy))
        dir_x = np.sign(dx)
        dir_y = np.sign(dy)
        
        x_mid = x1 + dir_x * dist_diag
        y_mid = y1 + dir_y * dist_diag
        
        segments.append([(x1, y1), (x_mid, y_mid)])
        segments.append([(x_mid, y_mid), (x2, y2)])
        
    # Draw traces
    lc = collections.LineCollection(segments, linewidths=2.0, colors="black", capstyle="round", joinstyle="round")
    ax.add_collection(lc)
    
    # Draw chips and vias
    for r, c in nodes:
        x = -10 + c * cell_size
        y = -10 + r * cell_size
        
        node_type = rng.choice(['via', 'chip', 'pad'])
        
        if node_type == 'via':
            c1 = patches.Circle((x, y), cell_size*0.4, facecolor='white', edgecolor='black', linewidth=2.0, zorder=3)
            ax.add_patch(c1)
        elif node_type == 'chip':
            rect = patches.Rectangle((x - cell_size*0.6, y - cell_size*0.6), cell_size*1.2, cell_size*1.2, 
                                     facecolor='black', zorder=3)
            ax.add_patch(rect)
        elif node_type == 'pad':
            rect = patches.Rectangle((x - cell_size*0.4, y - cell_size*0.4), cell_size*0.8, cell_size*0.8, 
                                     facecolor='none', edgecolor='black', linewidth=2.0, zorder=3)
            ax.add_patch(rect)

    save(fig, "abstract grid tessellation printed circuit board trace routing pattern black white texture")


if __name__ == "__main__":
    draw()
