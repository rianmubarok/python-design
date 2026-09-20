import numpy as np
import matplotlib.pyplot as plt
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
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
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
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def draw_star_8(cx, cy, outer_radius, inner_radius):
    """Draw an 8-pointed star (khatam)"""
    angles = []
    radii = []
    
    for i in range(16):  # 8 points × 2 (outer/inner)
        angle = i * np.pi / 8
        if i % 2 == 0:
            radius = outer_radius
        else:
            radius = inner_radius
        angles.append(angle)
        radii.append(radius)
    
    # Close the shape
    angles.append(angles[0])
    radii.append(radii[0])
    
    x = [cx + r * np.cos(a) for r, a in zip(radii, angles)]
    y = [cy + r * np.sin(a) for r, a in zip(radii, angles)]
    
    return x, y


def draw_interlaced_square(cx, cy, size, rotation=0):
    """Draw interlaced square pattern"""
    # Outer square
    angles1 = [np.pi/4 + i*np.pi/2 + rotation for i in range(5)]  # 5 to close
    x1 = [cx + size * np.cos(a) for a in angles1]
    y1 = [cy + size * np.sin(a) for a in angles1]
    
    # Inner rotated square
    angles2 = [np.pi/4 + i*np.pi/2 + rotation + np.pi/4 for i in range(5)]
    x2 = [cx + size * 0.7 * np.cos(a) for a in angles2]
    y2 = [cy + size * 0.7 * np.sin(a) for a in angles2]
    
    return (x1, y1), (x2, y2)


def arabesque_islamic_geometric():
    """
    Arabesque Islamic geometric pattern.
    Traditional Islamic geometric motifs with interlacing stars and polygons.
    """
    fig, ax = setup_ax()
    
    # Grid parameters for seamless tiling
    grid_size = 16
    cell_size = 100 / 6  # Divide canvas into 6×6 grid
    
    # Main pattern: 8-pointed stars with interlacing squares
    for row in range(-1, 8):
        for col in range(-1, 8):
            cx = col * cell_size + cell_size/2
            cy = row * cell_size + cell_size/2
            
            # Skip if outside extended canvas
            if cx < -10 or cx > 110 or cy < -10 or cy > 110:
                continue
            
            # Draw 8-pointed star
            star_outer = cell_size * 0.3
            star_inner = star_outer * 0.4
            
            x_star, y_star = draw_star_8(cx, cy, star_outer, star_inner)
            ax.plot(x_star, y_star, color="black", linewidth=1.5, solid_capstyle="round")
            
            # Draw interlaced squares around star
            square_size = cell_size * 0.25
            rotation_offset = (row + col) * np.pi / 8
            
            (x1, y1), (x2, y2) = draw_interlaced_square(cx, cy, square_size, rotation_offset)
            
            ax.plot(x1, y1, color="black", linewidth=1.2, solid_capstyle="round")
            ax.plot(x2, y2, color="black", linewidth=1.0, solid_capstyle="round")
    
    # Secondary pattern: connecting geometric elements
    # Rhombuses at intersection points
    for row in range(-1, 7):
        for col in range(-1, 7):
            # Intersection points between main grid
            int_x = (col + 0.5) * cell_size + cell_size/2
            int_y = (row + 0.5) * cell_size + cell_size/2
            
            if int_x < -5 or int_x > 105 or int_y < -5 or int_y > 105:
                continue
            
            # Draw small rhombus
            rhomb_size = cell_size * 0.15
            rhomb_angles = [0, np.pi/2, np.pi, 3*np.pi/2, 0]  # Diamond orientation
            
            x_rhomb = [int_x + rhomb_size * np.cos(a) for a in rhomb_angles]
            y_rhomb = [int_y + rhomb_size * np.sin(a) for a in rhomb_angles]
            
            ax.plot(x_rhomb, y_rhomb, color="black", linewidth=0.8, solid_capstyle="round")
    
    # Tertiary pattern: connecting lines and arabesques
    # Curved connecting elements
    for row in range(6):
        for col in range(6):
            cx = col * cell_size + cell_size/2
            cy = row * cell_size + cell_size/2
            
            # Draw connecting arcs to adjacent cells
            if col < 5:  # Right connection
                arc_start_x = cx + cell_size * 0.3
                arc_end_x = cx + cell_size * 0.7
                arc_y = cy
                
                # Create curved connection
                n_points = 10
                arc_x = np.linspace(arc_start_x, arc_end_x, n_points)
                arc_curve_y = arc_y + cell_size * 0.1 * np.sin(np.pi * np.linspace(0, 1, n_points))
                
                ax.plot(arc_x, arc_curve_y, color="black", linewidth=0.6, alpha=0.7)
            
            if row < 5:  # Down connection
                arc_start_y = cy + cell_size * 0.3
                arc_end_y = cy + cell_size * 0.7
                arc_x = cx
                
                # Create curved connection
                n_points = 10
                arc_y = np.linspace(arc_start_y, arc_end_y, n_points)
                arc_curve_x = arc_x + cell_size * 0.1 * np.sin(np.pi * np.linspace(0, 1, n_points))
                
                ax.plot(arc_curve_x, arc_y, color="black", linewidth=0.6, alpha=0.7)
    
    # Border decorative elements
    border_elements = [
        # Corner stars
        (cell_size * 0.5, cell_size * 0.5),
        (100 - cell_size * 0.5, cell_size * 0.5),
        (cell_size * 0.5, 100 - cell_size * 0.5),
        (100 - cell_size * 0.5, 100 - cell_size * 0.5)
    ]
    
    for bx, by in border_elements:
        # Small decorative 6-pointed stars
        star_6_outer = cell_size * 0.2
        star_6_inner = star_6_outer * 0.5
        
        angles_6 = []
        radii_6 = []
        
        for i in range(12):  # 6 points × 2
            angle = i * np.pi / 6
            if i % 2 == 0:
                radius = star_6_outer
            else:
                radius = star_6_inner
            angles_6.append(angle)
            radii_6.append(radius)
        
        angles_6.append(angles_6[0])
        radii_6.append(radii_6[0])
        
        x_6 = [bx + r * np.cos(a) for r, a in zip(radii_6, angles_6)]
        y_6 = [by + r * np.sin(a) for r, a in zip(radii_6, angles_6)]
        
        ax.plot(x_6, y_6, color="black", linewidth=1.0, solid_capstyle="round", alpha=0.8)
    
    save(fig, "arabesque islamic geometric")


if __name__ == "__main__":
    arabesque_islamic_geometric()