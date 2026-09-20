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
    Time Dilation Relativistic Space Warp Pattern.
    Concentric circles warped by relativistic effects including time dilation,
    length contraction, and spacetime curvature around massive objects.
    """
    fig, ax = setup_ax()
    
    cx, cy = 50.0, 50.0
    n_circles = 55
    max_radius = 75.0
    n_pts = 600
    
    # Relativistic parameters
    c = 299792458  # Speed of light (normalized)
    
    # Massive object parameters (causing spacetime curvature)
    mass_objects = [
        {"pos": np.array([50, 50]), "mass": 100, "velocity": 0.3},  # Central massive object
        {"pos": np.array([30, 70]), "mass": 30, "velocity": 0.7},   # Fast-moving object
        {"pos": np.array([70, 30]), "mass": 20, "velocity": 0.8},   # Ultra-relativistic object
    ]
    
    for i in range(1, n_circles + 1):
        time_step = i / n_circles  # Represents different times
        r_base = max_radius * time_step ** 1.2
        
        angles = np.linspace(0, 2 * np.pi, n_pts)
        x_pts = []
        y_pts = []
        
        for angle in angles:
            # Initial position in spacetime
            x_base = r_base * np.cos(angle)
            y_base = r_base * np.sin(angle)
            current_pos = np.array([cx + x_base, cy + y_base])
            
            total_warp = np.array([0.0, 0.0])
            time_dilation_factor = 1.0
            
            for obj in mass_objects:
                # Distance to massive object
                r_vec = current_pos - obj["pos"]
                r = np.linalg.norm(r_vec)
                r = max(r, 1.0)  # Avoid singularity
                
                # Schwarzschild radius (gravitational effects)
                rs = 2 * obj["mass"] / (c**2)  # Simplified
                
                # Time dilation due to gravity (gravitational time dilation)
                grav_time_dilation = np.sqrt(1 - rs / r)
                time_dilation_factor *= grav_time_dilation
                
                # Time dilation due to velocity (special relativity)
                gamma = 1 / np.sqrt(1 - (obj["velocity"])**2)
                time_dilation_factor *= (1 / gamma)
                
                # Spacetime curvature (geodesic deviation)
                curvature_strength = obj["mass"] / (r**2)
                
                # Gravitational lensing effect
                if r > rs:
                    deflection_angle = 4 * obj["mass"] / r  # Einstein deflection
                    lensing_factor = 1 + deflection_angle / (2 * np.pi)
                else:
                    lensing_factor = 2.0  # Strong field limit
                
                # Frame dragging (Lense-Thirring effect)
                frame_drag = 2 * obj["mass"] * obj["velocity"] / (r**3)
                drag_direction = np.array([-r_vec[1], r_vec[0]])  # Perpendicular
                if np.linalg.norm(drag_direction) > 0:
                    drag_direction = drag_direction / np.linalg.norm(drag_direction)
                
                # Combine relativistic effects
                radial_warp = curvature_strength * r_vec / r  # Gravitational attraction
                tangential_warp = frame_drag * drag_direction  # Frame dragging
                lensing_warp = (lensing_factor - 1) * r_vec / r  # Light bending
                
                total_warp += radial_warp + tangential_warp + lensing_warp
            
            # Apply time dilation to the pattern frequency
            temporal_modulation = np.sin(angle * 8 * time_dilation_factor + 
                                       time_step * 2 * np.pi * time_dilation_factor)
            
            # Length contraction effects (Lorentz contraction)
            # Assume motion in x-direction
            contraction_factor = 0.1 * (1 - time_dilation_factor)
            x_contraction = contraction_factor * np.cos(angle)
            
            # Apply relativistic warping
            warp_magnitude = min(np.linalg.norm(total_warp), 5.0)  # Limit extreme warping
            x_warped = x_base + total_warp[0] + x_contraction + 0.2 * temporal_modulation
            y_warped = y_base + total_warp[1] + 0.1 * temporal_modulation
            
            # Final position
            x_final = cx + x_warped
            y_final = cy + y_warped
            
            x_pts.append(x_final)
            y_pts.append(y_final)
        
        # Close the spacetime loop
        x_pts.append(x_pts[0])
        y_pts.append(y_pts[0])
        
        # Line width varies with time dilation
        lw = 0.4 + 1.0 * (2 - time_dilation_factor)  # Thicker lines where time is slower
        
        # Alpha varies with relativistic effects
        alpha = 0.6 + 0.4 * time_dilation_factor
        
        ax.plot(x_pts, y_pts, 'k-', linewidth=lw, alpha=alpha)
        
        # Add light ray paths (geodesics) every 8th circle
        if i % 8 == 0 and i > 16:
            n_rays = 12
            for ray in range(n_rays):
                ray_angle = ray * 2 * np.pi / n_rays
                
                # Trace light ray path through curved spacetime
                ray_points_x = []
                ray_points_y = []
                
                for t in np.linspace(0, 1, 20):
                    ray_r = r_base * (0.5 + 0.5 * t)
                    ray_x = cx + ray_r * np.cos(ray_angle)
                    ray_y = cy + ray_r * np.sin(ray_angle)
                    
                    # Apply spacetime curvature to light ray
                    ray_pos = np.array([ray_x, ray_y])
                    ray_warp = np.array([0.0, 0.0])
                    
                    for obj in mass_objects:
                        r_vec = ray_pos - obj["pos"]
                        r = np.linalg.norm(r_vec)
                        r = max(r, 1.0)
                        
                        # Light deflection
                        deflection = 2 * obj["mass"] / r * r_vec / r
                        ray_warp += deflection * 0.3
                    
                    ray_points_x.append(ray_x + ray_warp[0])
                    ray_points_y.append(ray_y + ray_warp[1])
                
                ax.plot(ray_points_x, ray_points_y, 'k-', linewidth=0.3, alpha=0.4)
    
    save(fig, "abstract concentric time dilation relativistic space warp pattern black white texture")

if __name__ == "__main__":
    draw()