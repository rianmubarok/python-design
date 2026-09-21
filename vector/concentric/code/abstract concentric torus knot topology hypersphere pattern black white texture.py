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
    Torus Knot Topology Hypersphere Pattern.
    Projects higher-dimensional torus knots onto 2D concentric circles,
    creating complex topological patterns with hypersphere intersections.
    """
    fig, ax = setup_ax()
    
    cx, cy = 50.0, 50.0
    n_circles = 45
    max_radius = 70.0
    n_pts = 800
    
    # Torus knot parameters
    p, q = 3, 5  # Trefoil-like knot (3,5)
    major_radius = 20.0
    minor_radius = 8.0
    
    # Hypersphere parameters (4D to 2D projection)
    w_rotation = 0.5  # 4th dimension rotation
    
    for i in range(1, n_circles + 1):
        r_base = max_radius * (i / n_circles) ** 1.1
        hypertime = i / n_circles  # 4D parameter evolution
        
        angles = np.linspace(0, 2 * np.pi, n_pts)
        x_pts = []
        y_pts = []
        
        for angle in angles:
            # Base circle position
            x_base = r_base * np.cos(angle)
            y_base = r_base * np.sin(angle)
            
            # Parametric torus knot in 4D
            t = angle  # Parameter along the knot
            
            # Torus knot coordinates in 4D
            torus_x = (major_radius + minor_radius * np.cos(q * t)) * np.cos(p * t)
            torus_y = (major_radius + minor_radius * np.cos(q * t)) * np.sin(p * t)
            torus_z = minor_radius * np.sin(q * t)
            torus_w = minor_radius * np.cos(p * t + hypertime * 2 * np.pi)  # 4th dimension
            
            # Hypersphere rotation in 4D space
            w_rot = w_rotation * hypertime
            torus_x_rot = torus_x * np.cos(w_rot) - torus_w * np.sin(w_rot)
            torus_w_rot = torus_x * np.sin(w_rot) + torus_w * np.cos(w_rot)
            
            # Project 4D to 2D (stereographic projection from hypersphere)
            projection_factor = 1 / (1 + torus_w_rot / 50)  # Avoid division by zero
            knot_x = torus_x_rot * projection_factor * 0.3
            knot_y = torus_y * projection_factor * 0.3
            knot_z_influence = torus_z * 0.2
            
            # Topological modulation based on knot geometry
            # Linking number effects
            linking_phase = p * angle + q * hypertime * 2 * np.pi
            linking_modulation = np.sin(linking_phase) * 0.15
            
            # Genus effects (topological complexity)
            genus_modulation = np.sin(angle * (p + q)) * np.cos(angle * abs(p - q)) * 0.1
            
            # Hypersphere intersection patterns
            sphere_intersection = np.sin(angle * 7 + hypertime * 4 * np.pi) * \
                                 np.cos(r_base * 0.1 + hypertime * np.pi) * 0.12
            
            # Combine topological effects
            total_topo_mod = linking_modulation + genus_modulation + \
                           sphere_intersection + knot_z_influence
            
            # Apply knot distortion to base circle
            x_final = cx + (x_base + knot_x) * (1 + total_topo_mod)
            y_final = cy + (y_base + knot_y) * (1 + total_topo_mod)
            
            x_pts.append(x_final)
            y_pts.append(y_final)
        
        # Close the topological loop
        x_pts.append(x_pts[0])
        y_pts.append(y_pts[0])
        
        # Line width varies with topological complexity
        complexity = abs(linking_modulation) + abs(genus_modulation)
        lw = 0.5 + 1.0 * min(complexity * 5, 1.5)
        
        ax.plot(x_pts, y_pts, 'k-', linewidth=lw, alpha=0.8)
        
        # Add knot crossing indicators
        if i % 7 == 0 and i > 14:
            for crossing in range(p * q):  # Number of crossings in (p,q) torus knot
                cross_t = crossing * 2 * np.pi / (p * q)
                
                # Calculate crossing position
                cross_torus_x = (major_radius + minor_radius * np.cos(q * cross_t)) * np.cos(p * cross_t)
                cross_torus_y = (major_radius + minor_radius * np.cos(q * cross_t)) * np.sin(p * cross_t)
                
                cross_x = cx + cross_torus_x * 0.3 * (r_base / max_radius)
                cross_y = cy + cross_torus_y * 0.3 * (r_base / max_radius)
                
                # Draw small crossing marker
                cross_size = 1.5
                ax.plot([cross_x - cross_size, cross_x + cross_size], 
                       [cross_y - cross_size, cross_y + cross_size], 'k-', linewidth=0.8, alpha=0.6)
                ax.plot([cross_x - cross_size, cross_x + cross_size], 
                       [cross_y + cross_size, cross_y - cross_size], 'k-', linewidth=0.8, alpha=0.6)
    
    save(fig, "abstract concentric torus knot topology hypersphere pattern black white texture")

if __name__ == "__main__":
    draw()