import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-1, 21)
    ax.set_ylim(-1, 21)
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


def abstract_grid_tessellation_hexagonal_truchet_tile_pattern_black_white_texture():
    """Generates a Hexagonal Truchet tiling pattern using concentric arcs."""
    fig, ax = setup_ax()
    
    # Hexagon parameters
    w = np.sqrt(3)
    h = 2
    
    n_cols = 15
    n_rows = 15
    
    for row in range(n_rows):
        for col in range(n_cols):
            # Calculate center of hexagon
            x = col * w
            if row % 2 != 0:
                x += w / 2
            y = row * (h * 0.75)
            
            # Truchet choice (3 possible rotations for the arcs connecting midpoints of edges)
            choice = np.random.choice([0, 1, 2])
            
            # Hexagon edge midpoints angles
            angles = [30, 90, 150, 210, 270, 330]
            
            pairs = []
            if choice == 0:
                pairs = [(30, 90), (150, 210), (270, 330)]
            elif choice == 1:
                pairs = [(90, 150), (210, 270), (330, 30)]
            else:
                pairs = [(330, 90), (150, 270)] # degenerate/straight lines, let's stick to true truchet curves
                # Alternate standard hexagonal truchet mapping (connect adjacent edges)
                pairs = [(330, 30), (90, 150), (210, 270)]
            
            if choice == 2:
                # Add straight lines connecting opposite edges for variety
                for a in [30, 90, 150]:
                    x1 = x + 0.5 * np.cos(np.radians(a))
                    y1 = y + 0.5 * np.sin(np.radians(a))
                    x2 = x + 0.5 * np.cos(np.radians(a + 180))
                    y2 = y + 0.5 * np.sin(np.radians(a + 180))
                    # Draw multiple parallel lines
                    for offset in np.linspace(-0.25, 0.25, 4):
                        perp_a = a + 90
                        ox = offset * np.cos(np.radians(perp_a))
                        oy = offset * np.sin(np.radians(perp_a))
                        ax.plot([x1+ox, x2+ox], [y1+oy, y2+oy], color="black", linewidth=1.5)
            else:
                # Draw arcs
                for (a1, a2) in pairs:
                    # Find corner between these two edges
                    corner_angle = (a1 + a2) / 2
                    if abs(a1 - a2) > 180:
                        corner_angle += 180
                        
                    cx = x + (1 / np.sqrt(3)) * np.cos(np.radians(corner_angle))
                    cy = y + (1 / np.sqrt(3)) * np.sin(np.radians(corner_angle))
                    
                    # Draw multiple concentric arcs
                    for r in np.linspace(0.1, 0.45, 4):
                        arc = Arc((cx, cy), 2*r, 2*r, angle=0, theta1=corner_angle+120, theta2=corner_angle+240, color="black", linewidth=1.5)
                        ax.add_patch(arc)
                        
    save(fig, "abstract grid tessellation hexagonal truchet tile pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_hexagonal_truchet_tile_pattern_black_white_texture()
