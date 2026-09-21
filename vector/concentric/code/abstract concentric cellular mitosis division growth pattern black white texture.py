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
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
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
    Cellular Mitosis Division Growth Pattern.
    Concentric circles that split and divide like cells undergoing mitosis,
    creating organic growth patterns with division lines and cellular boundaries.
    """
    fig, ax = setup_ax()
    
    cx, cy = 50.0, 50.0
    n_base_circles = 25
    max_radius = 65.0
    n_pts = 400
    
    for i in range(1, n_base_circles + 1):
        r_base = max_radius * (i / n_base_circles) ** 0.8
        
        # Determine number of cell divisions at this radius
        num_divisions = max(1, int(r_base / 8))  # More divisions as radius increases
        
        for division in range(num_divisions):
            # Calculate division angle offset
            division_angle = (2 * np.pi * division) / num_divisions
            
            # Create cell boundary with organic irregularity
            angles = np.linspace(0, 2 * np.pi, n_pts)
            x_pts = []
            y_pts = []
            
            for angle in angles:
                # Base cellular shape with organic variation
                organic_var = 0.15 * np.sin(angle * 5 + division_angle * 3) * np.cos(angle * 7)
                membrane_flutter = 0.08 * np.sin(angle * 12 + r_base * 0.3)
                
                # Cell growth pressure effects
                growth_pressure = 0.1 * np.sin(angle * 3 + division_angle) * (r_base / max_radius)
                
                radius_mod = r_base * (1 + organic_var + membrane_flutter + growth_pressure)
                
                # Add division line effects (cell wall formation)
                if num_divisions > 1:
                    division_effect = 0.05 * np.cos((angle - division_angle) * num_divisions * 2)
                    radius_mod *= (1 + division_effect)
                
                x = cx + radius_mod * np.cos(angle + division_angle)
                y = cy + radius_mod * np.sin(angle + division_angle)
                
                x_pts.append(x)
                y_pts.append(y)
            
            # Close the cell boundary
            x_pts.append(x_pts[0])
            y_pts.append(y_pts[0])
            
            # Variable line width based on cell maturity
            lw = 0.5 + 0.8 * (i / n_base_circles)
            ax.plot(x_pts, y_pts, 'k-', linewidth=lw, alpha=0.85)
            
            # Add division lines (mitotic spindles)
            if num_divisions > 1 and i > 5:  # Only for mature cells
                for div_line in range(num_divisions):
                    line_angle = (2 * np.pi * div_line) / num_divisions + division_angle
                    x1 = cx + (r_base * 0.3) * np.cos(line_angle)
                    y1 = cy + (r_base * 0.3) * np.sin(line_angle)
                    x2 = cx + (r_base * 0.9) * np.cos(line_angle)
                    y2 = cy + (r_base * 0.9) * np.sin(line_angle)
                    ax.plot([x1, x2], [y1, y2], 'k-', linewidth=0.3, alpha=0.6)
    
    save(fig, "abstract concentric cellular mitosis division growth pattern black white texture")

if __name__ == "__main__":
    draw()