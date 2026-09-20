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
    Magnetic Field Twisted Vortex Pattern.
    Combination of magnetic field effects with twisted vortex distortion,
    creating complex helical field patterns.
    """
    fig, ax = setup_ax()
    
    cx, cy = 50.0, 50.0
    n_circles = 50
    max_radius = 65.0
    n_pts = 800
    
    # Magnetic field parameters (multiple pole configuration)
    poles = [
        {"pos": np.array([35, 50]), "strength": 150, "polarity": 1},   # North
        {"pos": np.array([65, 50]), "strength": 150, "polarity": -1},  # South  
        {"pos": np.array([50, 35]), "strength": 100, "polarity": 1},   # North
        {"pos": np.array([50, 65]), "strength": 100, "polarity": -1},  # South
    ]
    
    # Vortex parameters
    vortex_center = np.array([50, 50])
    vortex_strength = 1.2
    twist_rate = 0.8  # How much the field lines twist
    
    for i in range(1, n_circles + 1):
        r_base = max_radius * (i / n_circles) ** 1.1
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        x_pts = []
        y_pts = []
        
        for j, angle in enumerate(angles):
            # Base position
            x_base = r_base * np.cos(angle)
            y_base = r_base * np.sin(angle)
            pt_canvas = np.array([cx + x_base, cy + y_base])
            
            # Calculate magnetic field effects
            magnetic_force = np.array([0.0, 0.0])
            for pole in poles:
                d_vec = pt_canvas - pole["pos"]
                dist = np.linalg.norm(d_vec)
                dist = max(dist, 2.0)  # Avoid division by zero
                
                # Magnetic field strength (inverse square law)
                field_strength = pole["polarity"] * pole["strength"] / (dist ** 2)
                field_direction = d_vec / dist
                magnetic_force += field_strength * field_direction
            
            # Calculate vortex twist effect
            d_vortex = pt_canvas - vortex_center
            vortex_dist = np.linalg.norm(d_vortex)
            
            if vortex_dist > 0:
                # Tangential vortex force
                tangent = np.array([-d_vortex[1], d_vortex[0]]) / vortex_dist
                vortex_force = vortex_strength * tangent * np.exp(-vortex_dist / 30)
                
                # Helical twist component
                twist_angle = twist_rate * angle + r_base * 0.1
                twist_amplitude = 0.3 * np.exp(-vortex_dist / 25)
                twist_force = twist_amplitude * np.array([
                    np.cos(twist_angle), 
                    np.sin(twist_angle)
                ])
                
                # Combine vortex effects
                total_vortex = vortex_force + twist_force
            else:
                total_vortex = np.array([0.0, 0.0])
            
            # Add field line curvature effects
            curvature_factor = 0.1 * np.sin(angle * 4 + r_base * 0.2)
            curvature_force = curvature_factor * np.array([
                -np.sin(angle), np.cos(angle)
            ])
            
            # Combine all forces
            total_displacement = magnetic_force * 0.05 + total_vortex + curvature_force
            
            # Apply displacement
            x_final = cx + x_base + total_displacement[0]
            y_final = cy + y_base + total_displacement[1]
            
            x_pts.append(x_final)
            y_pts.append(y_final)
        
        # Close the loop
        x_pts.append(x_pts[0])
        y_pts.append(y_pts[0])
        
        # Variable line width based on field strength
        field_intensity = np.linalg.norm(magnetic_force)
        lw = 0.5 + 1.0 * min(field_intensity / 50, 1.5)
        
        ax.plot(x_pts, y_pts, 'k-', linewidth=lw, alpha=0.8)
        
        # Add field direction indicators (every 10th circle)
        if i % 10 == 0 and i > 10:
            n_indicators = 16
            for k in range(n_indicators):
                ind_angle = k * 2 * np.pi / n_indicators
                x_pos = cx + r_base * 0.9 * np.cos(ind_angle)
                y_pos = cy + r_base * 0.9 * np.sin(ind_angle)
                
                # Calculate local field direction
                pt = np.array([x_pos, y_pos])
                local_field = np.array([0.0, 0.0])
                for pole in poles:
                    d_vec = pt - pole["pos"]
                    dist = np.linalg.norm(d_vec)
                    dist = max(dist, 2.0)
                    field_strength = pole["polarity"] * pole["strength"] / (dist ** 2)
                    local_field += field_strength * (d_vec / dist)
                
                # Normalize and draw field line
                if np.linalg.norm(local_field) > 0:
                    field_dir = local_field / np.linalg.norm(local_field)
                    arrow_length = 2.0
                    x_end = x_pos + arrow_length * field_dir[0]
                    y_end = y_pos + arrow_length * field_dir[1]
                    ax.plot([x_pos, x_end], [y_pos, y_end], 'k-', linewidth=0.5, alpha=0.6)
    
    save(fig, "abstract concentric magnetic field twisted vortex pattern black white texture")

if __name__ == "__main__":
    draw()