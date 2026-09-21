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
    Fractal Crystalline Growth Branching Pattern.
    Combines fractal recursive subcenters with crystalline growth patterns,
    creating branching dendrites that grow outward from multiple nucleation points.
    """
    fig, ax = setup_ax()
    
    cx, cy = 50.0, 50.0
    n_circles = 40
    max_radius = 72.0
    n_pts = 600
    
    # Crystalline growth parameters
    nucleation_points = []
    n_nuclei = 8
    for i in range(n_nuclei):
        angle = i * 2 * np.pi / n_nuclei
        dist = 15 + 10 * np.random.rand()
        nx = cx + dist * np.cos(angle)
        ny = cy + dist * np.sin(angle)
        nucleation_points.append({
            "pos": np.array([nx, ny]),
            "strength": 0.5 + 0.5 * np.random.rand(),
            "branch_angle": angle,
            "growth_rate": 0.8 + 0.4 * np.random.rand()
        })
    
    # Fractal recursion parameters
    recursion_centers = [
        {"pos": np.array([cx-15, cy-10]), "scale": 0.3, "phase": 0},
        {"pos": np.array([cx+12, cy-15]), "scale": 0.4, "phase": np.pi/3},
        {"pos": np.array([cx-8, cy+18]), "scale": 0.35, "phase": 2*np.pi/3},
        {"pos": np.array([cx+20, cy+8]), "scale": 0.25, "phase": np.pi},
    ]
    
    for i in range(1, n_circles + 1):
        growth_stage = i / n_circles
        r_base = max_radius * growth_stage ** 1.2
        
        angles = np.linspace(0, 2 * np.pi, n_pts)
        x_pts = []
        y_pts = []
        
        for angle in angles:
            x_base = r_base * np.cos(angle)
            y_base = r_base * np.sin(angle)
            current_pos = np.array([cx + x_base, cy + y_base])
            
            # Crystalline growth effects
            crystal_modulation = 0
            for nucleus in nucleation_points:
                # Distance to nucleation point
                dist_to_nucleus = np.linalg.norm(current_pos - nucleus["pos"])
                
                # Growth direction bias (dendrite branching)
                growth_direction = current_pos - nucleus["pos"]
                if np.linalg.norm(growth_direction) > 0:
                    growth_direction = growth_direction / np.linalg.norm(growth_direction)
                
                # Crystalline faceting (preferred growth directions)
                facet_angles = [0, np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3]  # 6-fold symmetry
                facet_influence = 0
                for facet_angle in facet_angles:
                    facet_dir = np.array([np.cos(nucleus["branch_angle"] + facet_angle), 
                                        np.sin(nucleus["branch_angle"] + facet_angle)])
                    alignment = np.dot(growth_direction, facet_dir)
                    facet_influence += 0.1 * max(alignment, 0) ** 2
                
                # Dendrite branching pattern
                branch_freq = 6 + 2 * int(nucleus["strength"] * 4)  # Variable branching
                branch_pattern = np.sin(angle * branch_freq + nucleus["branch_angle"]) ** 2
                
                # Growth rate modulation
                growth_factor = nucleus["strength"] * nucleus["growth_rate"] * growth_stage
                distance_decay = np.exp(-dist_to_nucleus / 20)
                
                crystal_modulation += (facet_influence + 0.2 * branch_pattern) * growth_factor * distance_decay
            
            # Fractal recursive modulation
            fractal_modulation = 0
            for center in recursion_centers:
                # Distance to fractal center
                dist_to_center = np.linalg.norm(current_pos - center["pos"])
                
                # Recursive scaling pattern
                scale_factor = center["scale"]
                local_angle = np.arctan2(current_pos[1] - center["pos"][1], 
                                       current_pos[0] - center["pos"][0])
                
                # Multi-scale recursive pattern
                for scale_level in range(3):
                    scale = scale_factor ** (scale_level + 1)
                    freq = 8 * (2 ** scale_level)
                    recursive_pattern = np.sin(local_angle * freq + center["phase"]) * scale
                    distance_weight = np.exp(-dist_to_center / (30 * scale_factor))
                    fractal_modulation += recursive_pattern * distance_weight
            
            # Combine crystalline and fractal effects
            total_modulation = crystal_modulation + 0.3 * fractal_modulation
            
            # Apply growth boundaries (simulate crystal edges)
            boundary_effect = 0.05 * np.sin(angle * 12 + r_base * 0.4) * growth_stage
            
            # Final radius calculation
            radius_final = r_base * (1 + 0.4 * total_modulation + boundary_effect)
            
            x_final = cx + radius_final * np.cos(angle)
            y_final = cy + radius_final * np.sin(angle)
            
            x_pts.append(x_final)
            y_pts.append(y_final)
        
        # Close the loop
        x_pts.append(x_pts[0])
        y_pts.append(y_pts[0])
        
        # Variable line width based on crystal maturity
        crystal_density = abs(crystal_modulation) + abs(fractal_modulation)
        lw = 0.4 + 1.2 * min(crystal_density, 1.0) * growth_stage
        
        ax.plot(x_pts, y_pts, 'k-', linewidth=lw, alpha=0.85)
        
        # Add crystalline growth directions (dendrite arms)
        if i % 8 == 0 and i > 16:
            for nucleus in nucleation_points:
                if nucleus["strength"] > 0.6:  # Only strong nuclei
                    for branch in range(6):  # 6-fold crystal symmetry
                        branch_angle = nucleus["branch_angle"] + branch * np.pi / 3
                        
                        # Branch length based on growth stage
                        branch_length = 8 * growth_stage * nucleus["strength"]
                        
                        x1 = nucleus["pos"][0]
                        y1 = nucleus["pos"][1]
                        x2 = x1 + branch_length * np.cos(branch_angle)
                        y2 = y1 + branch_length * np.sin(branch_angle)
                        
                        ax.plot([x1, x2], [y1, y2], 'k-', linewidth=0.4, alpha=0.4)
    
    save(fig, "abstract concentric fractal crystalline growth branching pattern black white texture")

if __name__ == "__main__":
    draw()