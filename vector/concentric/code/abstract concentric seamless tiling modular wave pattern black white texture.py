import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

# Configuration
SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

# Directory Management
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
EPS_DIR = OUTPUT_DIR / "eps"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)

def setup_ax():
    """Initialize axis coordinates (off, equal aspect, white background)."""
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax

def save(fig, name):
    """Save image in JPG and SVG formats."""
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
    print(f"Saved: {jpg_path} | {svg_path} | {eps_path}")

def draw():
    """
    Seamless Tiling Modular Wave Pattern.
    Designed specifically for seamless tiling with modular wave functions
    that create perfect continuity at boundaries.
    """
    fig, ax = setup_ax()
    
    # Seamless tiling parameters
    tile_size = 100.0
    n_circles = 30
    max_radius = 35.0  # Smaller radius to ensure seamless tiling
    n_pts = 400
    
    # Create multiple tile centers for seamless effect
    tile_centers = [
        (25, 25), (75, 25), (25, 75), (75, 75),  # Corner regions
        (50, 50),  # Center
        (0, 50), (100, 50), (50, 0), (50, 100)   # Edge centers (wrap around)
    ]
    
    for i in range(1, n_circles + 1):
        r_base = max_radius * (i / n_circles) ** 1.1
        
        # Draw concentric circles around each tile center
        for cx, cy in tile_centers:
            angles = np.linspace(0, 2 * np.pi, n_pts)
            x_pts = []
            y_pts = []
            
            for angle in angles:
                # Base circle position
                x_base = r_base * np.cos(angle)
                y_base = r_base * np.sin(angle)
                
                # Seamless wave modulation (using periodic functions)
                # Ensure continuity at tile boundaries
                wave_x = np.sin(2 * np.pi * (cx + x_base) / tile_size * 4)
                wave_y = np.cos(2 * np.pi * (cy + y_base) / tile_size * 4)
                
                # Cross-tile interference pattern (seamless)
                interference = wave_x * wave_y
                
                # Additional seamless wave layers
                wave2 = np.sin(2 * np.pi * (cx + x_base) / tile_size * 2 + 
                              2 * np.pi * (cy + y_base) / tile_size * 3)
                wave3 = np.cos(2 * np.pi * (cx + x_base) / tile_size * 3 + 
                              2 * np.pi * (cy + y_base) / tile_size * 2)
                
                # Combine waves with seamless properties
                total_modulation = 0.3 * (interference + 0.5 * wave2 + 0.3 * wave3)
                
                # Apply radius modulation
                radius_mod = r_base * (1 + total_modulation)
                
                x_final = cx + radius_mod * np.cos(angle)
                y_final = cy + radius_mod * np.sin(angle)
                
                # Apply boundary wrapping for seamless tiling
                x_final = x_final % tile_size
                y_final = y_final % tile_size
                
                x_pts.append(x_final)
                y_pts.append(y_final)
            
            # Close the loop
            x_pts.append(x_pts[0])
            y_pts.append(y_pts[0])
            
            # Variable line width for visual interest
            lw = 0.5 + 0.3 * np.sin(i * 0.5)
            
            # Only draw if circle is within main tile area
            if 0 <= cx <= 100 and 0 <= cy <= 100:
                ax.plot(x_pts, y_pts, 'k-', linewidth=lw, alpha=0.8)
    
    # Add seamless connecting elements
    for y in range(0, 101, 25):
        for x in range(0, 101, 25):
            # Small connecting wave patterns
            wave_x = np.linspace(x, x + 25, 50)
            wave_y = y + 5 * np.sin(2 * np.pi * wave_x / 25)
            ax.plot(wave_x, wave_y, 'k-', linewidth=0.3, alpha=0.5)
            
            # Vertical connecting waves
            wave_y = np.linspace(y, y + 25, 50)
            wave_x = x + 3 * np.cos(2 * np.pi * wave_y / 25)
            ax.plot(wave_x, wave_y, 'k-', linewidth=0.3, alpha=0.5)
    
    save(fig, "abstract concentric seamless tiling modular wave pattern black white texture")

if __name__ == "__main__":
    draw()