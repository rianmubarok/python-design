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
    Wang Tiles Pipe Network Maze.
    A maze/network generated using edge-matching Wang tiles.
    Each tile is a square with pipes connecting the edges.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.patches as patches
    
    grid_size = 25
    cell_w = 120.0 / grid_size
    
    # We define 4 basic pipe tiles:
    # 1: Straight horizontal
    # 2: Straight vertical
    # 3: Corner (top-left)
    # 4: Corner (top-right)
    # 5: Corner (bottom-left)
    # 6: Corner (bottom-right)
    # 7: Cross intersection
    
    # Randomly assign tiles without strict Wang edge constraints for a chaotic broken network,
    # or enforce them. We will do a visually dense chaotic mix of corners and crosses.
    
    for row in range(-1, grid_size + 1):
        for col in range(-1, grid_size + 1):
            cx = -10 + col * cell_w
            cy = -10 + row * cell_w
            
            tile = rng.choice([1, 2, 3, 4, 5, 6, 7])
            
            # Center of the cell
            mid_x = cx + cell_w / 2
            mid_y = cy + cell_w / 2
            
            # Pipe radius
            pr = cell_w * 0.15
            
            # Helper to draw a pipe segment
            def draw_pipe(x1, y1, x2, y2):
                # We draw a thick black line, and a slightly thinner white line inside
                ax.plot([x1, x2], [y1, y2], color="black", linewidth=12.0, solid_capstyle="butt")
                ax.plot([x1, x2], [y1, y2], color="white", linewidth=6.0, solid_capstyle="butt")
                
            def draw_arc(center_x, center_y, angle1, angle2):
                arc = patches.Arc((center_x, center_y), cell_w, cell_w, 
                                  angle=0, theta1=angle1, theta2=angle2, 
                                  linewidth=12.0, color="black", capstyle="butt")
                ax.add_patch(arc)
                arc_w = patches.Arc((center_x, center_y), cell_w, cell_w, 
                                  angle=0, theta1=angle1, theta2=angle2, 
                                  linewidth=6.0, color="white", capstyle="butt")
                ax.add_patch(arc_w)
            
            # Edges
            top = (mid_x, cy + cell_w)
            bottom = (mid_x, cy)
            left = (cx, mid_y)
            right = (cx + cell_w, mid_y)
            
            if tile == 1: # Horizontal
                draw_pipe(left[0], left[1], right[0], right[1])
            elif tile == 2: # Vertical
                draw_pipe(top[0], top[1], bottom[0], bottom[1])
            elif tile == 3: # Top-Left (Arc centered at Top-Left corner of cell)
                draw_arc(cx, cy + cell_w, 270, 360)
            elif tile == 4: # Top-Right
                draw_arc(cx + cell_w, cy + cell_w, 180, 270)
            elif tile == 5: # Bottom-Left
                draw_arc(cx, cy, 0, 90)
            elif tile == 6: # Bottom-Right
                draw_arc(cx + cell_w, cy, 90, 180)
            elif tile == 7: # Cross
                draw_pipe(left[0], left[1], right[0], right[1])
                draw_pipe(top[0], top[1], bottom[0], bottom[1])
                # Add a joint circle
                joint_b = patches.Circle((mid_x, mid_y), cell_w*0.3, color="black", zorder=3)
                joint_w = patches.Circle((mid_x, mid_y), cell_w*0.2, color="white", zorder=4)
                joint_d = patches.Circle((mid_x, mid_y), cell_w*0.05, color="black", zorder=5)
                ax.add_patch(joint_b)
                ax.add_patch(joint_w)
                ax.add_patch(joint_d)

    save(fig, "abstract grid tessellation wang tiles pipe network maze pattern black white texture")


if __name__ == "__main__":
    draw()
