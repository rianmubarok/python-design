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
    Ripple Interference Micro-Macro Scale Pattern.
    Variation of ripple interference with multiple scales - from microscopic
    to macroscopic interference patterns creating a fractal-like complexity.
    """
    fig, ax = setup_ax()
    
    cx, cy = 50.0, 50.0
    n_circles = 60
    max_radius = 70.0
    n_pts = 700
    
    # Multi-scale interference sources
    macro_sources = [(35, 45), (65, 55)]  # Large-scale sources
    micro_sources = [(45, 40), (55, 60), (40, 60), (60, 40)]  # Small-scale sources
    nano_sources = []  # Microscopic scale
    for _ in range(12):
        angle = np.random.rand() * 2 * np.pi
        radius = 15 + np.random.rand() * 25
        nano_x = cx + radius * np.cos(angle)
        nano_y = cy + radius * np.sin(angle)
        nano_sources.append((nano_x, nano_y))
    
    for i in range(1, n_circles + 1):
        r_base = max_radius * (i / n_circles) ** 0.9
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        x_pts = []
        y_pts = []
        
        for angle in angles:
            x_base = cx + r_base * np.cos(angle)
            y_base = cy + r_base * np.sin(angle)
            
            # Macro-scale interference (large wavelength)
            macro_interference = 0
            for src_x, src_y in macro_sources:
                dist = np.sqrt((x_base - src_x)**2 + (y_base - src_y)**2)
                macro_interference += np.sin(dist * 0.8) * 0.4
            
            # Micro-scale interference (medium wavelength)
            micro_interference = 0
            for src_x, src_y in micro_sources:
                dist = np.sqrt((x_base - src_x)**2 + (y_base - src_y)**2)
                micro_interference += np.sin(dist * 2.5) * 0.2
            
            # Nano-scale interference (high frequency)
            nano_interference = 0
            for src_x, src_y in nano_sources:
                dist = np.sqrt((x_base - src_x)**2 + (y_base - src_y)**2)
                nano_interference += np.sin(dist * 6.0) * 0.1
            
            # Scale-dependent amplitude modulation
            scale_factor = 1 + 0.1 * np.sin(r_base * 0.3)
            
            # Combine all scales with different phase relationships
            total_interference = (macro_interference + 
                                micro_interference * scale_factor + 
                                nano_interference * scale_factor**2)
            
            # Apply interference to radius
            radius_final = r_base * (1 + 0.3 * total_interference)
            
            x_final = cx + radius_final * np.cos(angle)
            y_final = cy + radius_final * np.sin(angle)
            
            x_pts.append(x_final)
            y_pts.append(y_final)
        
        # Close the loop
        x_pts.append(x_pts[0])
        y_pts.append(y_pts[0])
        
        # Dynamic line width based on interference complexity
        complexity = abs(macro_interference) + abs(micro_interference) + abs(nano_interference)
        lw = 0.4 + 0.8 * min(complexity, 1.0)
        
        ax.plot(x_pts, y_pts, 'k-', linewidth=lw, alpha=0.85)
    
    save(fig, "abstract concentric ripple interference micro macro scale pattern black white texture")

if __name__ == "__main__":
    draw()