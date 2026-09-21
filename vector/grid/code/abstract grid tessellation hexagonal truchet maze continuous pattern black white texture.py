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
    Hexagonal Truchet Maze.
    A continuous maze generated on a hexagonal grid using hexagonal Truchet tiles.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.patches as patches

    hex_size = 4.0
    h = hex_size * np.sqrt(3) / 2.0
    
    cols = int(120 / (hex_size * 1.5)) + 2
    rows = int(120 / h) + 2

    # A hexagonal Truchet tile has 3 arcs connecting the 6 midpoints of the hexagon.
    # There are multiple configurations, but linking adjacent midpoints forms tiny loops,
    # and linking opposite midpoints forms straight lines across.
    # Let's link them by drawing arcs between adjacent midpoints.
    # The midpoints of a flat-topped hexagon are at angles: 30, 90, 150, 210, 270, 330
    
    for row in range(-2, rows):
        for col in range(-2, cols):
            cx = col * hex_size * 1.5
            cy = row * h * 2.0
            if col % 2 != 0:
                cy += h
                
            # Randomly select a rotation for the internal arcs (0, 60, or 120 degrees)
            rotation = rng.choice([0, 60, 120])
            
            # The arcs connect midpoints.
            # Arc 1: connects midpoint at 30 to midpoint at 90.
            # Center of this arc is the hexagon corner between them (at 60 degrees).
            # The radius of this arc is hex_size / 2.
            
            arc_radius = hex_size / 2
            
            for base_angle in [60, 180, 300]:
                corner_angle = base_angle + rotation
                rad = np.radians(corner_angle)
                corner_x = cx + hex_size * np.cos(rad)
                corner_y = cy + hex_size * np.sin(rad)
                
                # Draw arc centered at corner_x, corner_y
                # Start and end angles of the arc depend on the corner
                # E.g., if corner is at 60, arcs go from 210 to 270 (towards the center)
                arc_start = corner_angle + 150
                arc_end = corner_angle + 210
                
                arc = patches.Arc((corner_x, corner_y), arc_radius*2, arc_radius*2,
                                  angle=0, theta1=arc_start, theta2=arc_end,
                                  linewidth=3.0, color="black", capstyle="round")
                ax.add_patch(arc)

    save(fig, "abstract grid tessellation hexagonal truchet maze continuous pattern black white texture")


if __name__ == "__main__":
    draw()
