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
EPS_DIR = OUTPUT_DIR / "eps"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    eps_path = EPS_DIR / f"{name} {DATE}.eps"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    # Save EPS with larger figure size for 4MP+ bounding box
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format="eps", pad_inches=0, facecolor="white", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path} | {eps_path}")


def draw_hexagon(cx, cy, radius):
    """Draw a hexagon centered at (cx, cy) with given radius."""
    angles = np.array([np.pi/6 + np.pi*k/3 for k in range(7)])  # 7 points to close
    x = cx + radius * np.cos(angles)
    y = cy + radius * np.sin(angles)
    return x, y


def draw():
    """
    Geometric Tessellation Honeycomb Hexagon Seamless.
    Concentric hexagonal tessellation pattern with varying sizes,
    designed for seamless tiling across multiple repetitions.
    """
    fig, ax = setup_ax()

    # Hexagon grid parameters for seamless tiling
    hex_width = np.sqrt(3)  # Width of hexagon in grid units
    hex_height = 1.5  # Height spacing in grid units
    
    # Scale factor for the canvas
    scale = 8.0
    
    # Number of hexagon layers (concentric rings)
    n_layers = 5
    
    # Generate hexagonal grid positions
    grid_positions = []
    
    # Center hexagon
    grid_positions.append((0, 0))
    
    # Add concentric hexagonal rings
    for layer in range(1, n_layers + 1):
        for side in range(6):  # 6 sides of hexagon
            for step in range(layer):
                # Calculate position for each hexagon in the ring
                if side == 0:  # Right edge
                    x = layer - step
                    y = step
                elif side == 1:  # Upper right
                    x = -step
                    y = layer
                elif side == 2:  # Upper left
                    x = -layer
                    y = layer - step
                elif side == 3:  # Left edge
                    x = -layer + step
                    y = -step
                elif side == 4:  # Lower left
                    x = step
                    y = -layer
                elif side == 5:  # Lower right
                    x = layer
                    y = -layer + step
                
                grid_positions.append((x, y))
    
    # Convert grid coordinates to canvas coordinates
    for gx, gy in grid_positions:
        # Hexagonal grid coordinate conversion
        cx = 50 + scale * (hex_width * (gx + gy * 0.5))
        cy = 50 + scale * (hex_height * gy)
        
        # Calculate distance from center for radius variation
        dist_from_center = np.sqrt(gx*gx + gy*gy + gx*gy)  # Hexagonal distance
        
        # Radius varies with distance from center
        base_radius = 3.5
        radius = base_radius * (1.0 + 0.3 * np.sin(dist_from_center * np.pi / 2))
        
        # Only draw if within canvas bounds
        if -10 <= cx <= 110 and -10 <= cy <= 110:
            x_hex, y_hex = draw_hexagon(cx, cy, radius)
            
            # Line properties vary with layer
            if dist_from_center == 0:  # Center hexagon
                lw = 2.5
            elif int(dist_from_center) % 2 == 0:  # Even layers
                lw = 1.8
            else:  # Odd layers
                lw = 1.2
            
            ax.plot(x_hex, y_hex, color="black", linewidth=lw, solid_capstyle="round", solid_joinstyle="round")

    save(fig, "abstract concentric geometric tessellation honeycomb hexagon seamless pattern black white texture")


if __name__ == "__main__":
    draw()