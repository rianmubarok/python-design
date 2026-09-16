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
    Circular Labyrinth Maze.
    Concentric rings with random gaps, connected by radial lines (walls),
    forming a complex labyrinth structure.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    cx, cy = 50.0, 50.0
    n_circles = 30
    max_radius = 65.0
    
    # Track the angular locations of walls to connect gaps
    # For a true maze we need a spanning tree, but visually we can just 
    # generate random arcs and connect their endpoints radially.

    prev_nodes = []
    
    for i in range(1, n_circles + 1):
        r = max_radius * (i / n_circles)
        
        # Number of segments in this ring
        n_segments = int(3 + i * 0.8)
        
        start_angles = np.sort(rng.uniform(0, 2 * np.pi, n_segments))
        
        current_nodes = []
        
        for j in range(n_segments):
            start = start_angles[j]
            end = start_angles[(j + 1) % n_segments]
            
            if end < start:
                end += 2 * np.pi
                
            # Leave a small gap
            gap = 0.15
            end -= gap
            if end <= start:
                continue
                
            angles = np.linspace(start, end, 50)
            ax.plot(cx + r * np.cos(angles), cy + r * np.sin(angles), 
                    color="black", linewidth=2.0, solid_capstyle="round")
                    
            current_nodes.append((start, end, r))
            
        # Draw radial walls connecting to previous ring
        if i > 1:
            for s, e, r_cur in current_nodes:
                # Randomly place a radial wall dropping down to the previous ring
                # between start and end of this segment
                if rng.random() > 0.3 and (e - s) > 0.12:
                    wall_angle = rng.uniform(s + 0.05, e - 0.05)
                    r_prev = max_radius * ((i - 1) / n_circles)
                    ax.plot([cx + r_prev * np.cos(wall_angle), cx + r_cur * np.cos(wall_angle)],
                            [cy + r_prev * np.sin(wall_angle), cy + r_cur * np.sin(wall_angle)],
                            color="black", linewidth=2.0, solid_capstyle="round")

    save(fig, "abstract concentric labyrinth circular maze pattern black white texture")


if __name__ == "__main__":
    draw()
