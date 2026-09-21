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
    Sonic Boom Shockwave Propagation Pattern.
    Concentric circles representing shockwaves with compression zones,
    Mach cone effects, and supersonic disturbances.
    """
    fig, ax = setup_ax()
    
    cx, cy = 50.0, 50.0
    n_waves = 45
    max_radius = 75.0
    n_pts = 600
    
    # Sonic parameters
    mach_number = 2.5  # Supersonic speed ratio
    compression_zones = 5  # Number of major compression regions
    
    for i in range(1, n_waves + 1):
        r_base = max_radius * (i / n_waves) ** 1.1
        
        # Shockwave intensity decreases with distance
        wave_intensity = np.exp(-r_base / (max_radius * 0.7))
        
        angles = np.linspace(0, 2 * np.pi, n_pts)
        x_pts = []
        y_pts = []
        
        for angle in angles:
            # Mach cone distortion (directional shockwave)
            mach_effect = 0.2 * np.cos(angle) * wave_intensity / mach_number
            
            # Compression zones (periodic pressure waves)
            compression = 0
            for zone in range(compression_zones):
                zone_freq = (zone + 1) * 2
                compression += (0.1 / (zone + 1)) * np.sin(r_base * zone_freq / 10) * wave_intensity
            
            # High-frequency pressure oscillations
            pressure_oscillation = 0.05 * np.sin(r_base * 3 + angle * 8) * wave_intensity
            
            # Atmospheric density variation effects
            density_effect = 0.08 * np.sin(angle * 4 + r_base * 0.5) * wave_intensity
            
            # Combine all shockwave effects
            total_distortion = mach_effect + compression + pressure_oscillation + density_effect
            radius_final = r_base * (1 + total_distortion)
            
            x = cx + radius_final * np.cos(angle)
            y = cy + radius_final * np.sin(angle)
            
            x_pts.append(x)
            y_pts.append(y)
        
        # Close the shockwave
        x_pts.append(x_pts[0])
        y_pts.append(y_pts[0])
        
        # Line width varies with wave intensity and compression
        base_compression = np.mean([np.sin(r_base * (z+1) * 2 / 10) for z in range(compression_zones)])
        lw = 0.4 + 1.2 * wave_intensity * (1 + 0.5 * abs(base_compression))
        
        # Alpha varies with distance for atmospheric scattering effect
        alpha = 0.7 + 0.3 * wave_intensity
        
        ax.plot(x_pts, y_pts, 'k-', linewidth=lw, alpha=alpha)
        
        # Add directional shock lines (Mach cone visualization)
        if i % 8 == 0 and wave_intensity > 0.3:
            cone_angle = np.arcsin(1 / mach_number)  # Mach cone half-angle
            for direction in [-1, 1]:
                shock_angle = direction * cone_angle
                x1 = cx + (r_base * 0.2) * np.cos(shock_angle)
                y1 = cy + (r_base * 0.2) * np.sin(shock_angle)
                x2 = cx + (r_base * 1.1) * np.cos(shock_angle)
                y2 = cy + (r_base * 1.1) * np.sin(shock_angle)
                ax.plot([x1, x2], [y1, y2], 'k-', linewidth=0.8 * wave_intensity, alpha=0.5)
    
    save(fig, "abstract concentric sonic boom shockwave propagation pattern black white texture")

if __name__ == "__main__":
    draw()