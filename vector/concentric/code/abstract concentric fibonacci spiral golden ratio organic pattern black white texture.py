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
    Fibonacci Spiral Golden Ratio Organic Pattern.
    Combines existing spiral concept with Fibonacci sequences and golden ratio
    proportions, creating naturally occurring organic growth patterns.
    """
    fig, ax = setup_ax()
    
    cx, cy = 50.0, 50.0
    n_circles = 50
    max_radius = 68.0
    n_pts = 500
    
    # Golden ratio and Fibonacci parameters
    phi = (1 + np.sqrt(5)) / 2  # Golden ratio
    fibonacci_seq = [1, 1]
    for i in range(30):  # Generate Fibonacci sequence
        fibonacci_seq.append(fibonacci_seq[-1] + fibonacci_seq[-2])
    
    # Organic growth parameters
    growth_centers = []
    n_growth_points = 8
    for i in range(n_growth_points):
        angle = i * 2 * np.pi / n_growth_points
        # Distance based on golden ratio
        dist = 20 * (phi ** (i % 4 - 2))  # Varies with golden ratio powers
        gx = cx + dist * np.cos(angle)
        gy = cy + dist * np.sin(angle)
        growth_centers.append({
            "pos": np.array([gx, gy]),
            "fib_index": i % len(fibonacci_seq),
            "phi_power": (i % 8) - 4
        })
    
    for i in range(1, n_circles + 1):
        growth_stage = i / n_circles
        
        # Fibonacci spacing (circles spaced according to Fibonacci ratios)
        fib_index = min(i - 1, len(fibonacci_seq) - 1)
        fib_ratio = fibonacci_seq[fib_index] / fibonacci_seq[min(fib_index + 1, len(fibonacci_seq) - 1)]
        
        r_base = max_radius * growth_stage ** (1 + 0.2 * np.sin(fib_ratio * np.pi))
        
        angles = np.linspace(0, 2 * np.pi, n_pts)
        x_pts = []
        y_pts = []
        
        for angle in angles:
            x_base = r_base * np.cos(angle)
            y_base = r_base * np.sin(angle)
            
            # Golden ratio spiral modulation
            # Convert angle to spiral parameter
            spiral_param = angle + growth_stage * 2 * np.pi
            
            # Multiple nested golden spirals
            spiral_modulations = []
            for spiral_idx in range(3):
                spiral_phase = spiral_idx * 2 * np.pi / 3
                spiral_radius = np.exp(spiral_param / (phi + spiral_idx))
                spiral_mod = 0.15 * np.sin(spiral_radius + spiral_phase) / (spiral_idx + 1)
                spiral_modulations.append(spiral_mod)
            
            # Fibonacci angle relationships (137.5 degrees)
            golden_angle = 2 * np.pi * (phi - 1)  # ~137.5 degrees
            fib_pattern = 0.12 * np.sin(angle / golden_angle * fibonacci_seq[fib_index % 10])
            
            # Organic growth from multiple centers
            organic_modulation = 0
            for center in growth_centers:
                distance = np.linalg.norm(np.array([cx + x_base, cy + y_base]) - center["pos"])
                
                # Growth influence based on Fibonacci numbers
                fib_strength = fibonacci_seq[center["fib_index"]] / 100.0
                
                # Golden ratio scaling
                phi_scale = phi ** center["phi_power"] / 10.0
                
                # Organic growth pattern (like leaf veins or tree branches)
                growth_direction = np.array([cx + x_base, cy + y_base]) - center["pos"]
                if np.linalg.norm(growth_direction) > 0:
                    growth_direction = growth_direction / np.linalg.norm(growth_direction)
                
                # Branching pattern based on golden angle
                branch_angles = []
                for branch in range(5):  # Pentagonal symmetry (related to golden ratio)
                    branch_angle = branch * golden_angle
                    branch_dir = np.array([np.cos(branch_angle), np.sin(branch_angle)])
                    alignment = np.dot(growth_direction, branch_dir)
                    if alignment > 0.5:  # Strong alignment with branch direction
                        branch_influence = fib_strength * phi_scale * alignment
                        organic_modulation += branch_influence * np.exp(-distance / 15)
            
            # Phyllotaxis pattern (spiral arrangement of leaves/seeds)
            phyllotaxis_angle = angle * golden_angle
            phyllotaxis_pattern = 0.1 * np.sin(phyllotaxis_angle) * np.cos(phyllotaxis_angle / phi)
            
            # Natural resonance frequencies (based on golden ratio harmonics)
            resonance = 0
            for harmonic in range(3):
                freq = phi ** harmonic
                resonance += 0.08 * np.sin(angle * freq + growth_stage * 2 * np.pi) / (harmonic + 1)
            
            # Combine all organic modulations
            total_modulation = (sum(spiral_modulations) + fib_pattern + organic_modulation + 
                              phyllotaxis_pattern + resonance)
            
            # Apply natural growth boundaries
            growth_boundary = 1 + 0.1 * np.sin(angle * 8 + growth_stage * phi * 2 * np.pi)
            
            # Final radius with organic growth
            radius_final = r_base * growth_boundary * (1 + total_modulation)
            
            x_final = cx + radius_final * np.cos(angle)
            y_final = cy + radius_final * np.sin(angle)
            
            x_pts.append(x_final)
            y_pts.append(y_final)
        
        # Close the organic loop
        x_pts.append(x_pts[0])
        y_pts.append(y_pts[0])
        
        # Line width based on Fibonacci growth
        fib_weight = fibonacci_seq[fib_index % 10] / max(fibonacci_seq[:10])
        lw = 0.5 + 1.0 * fib_weight * growth_stage
        
        ax.plot(x_pts, y_pts, 'k-', linewidth=lw, alpha=0.85)
        
        # Add golden spiral guides (every 8th circle)
        if i % 8 == 0 and i > 16:
            # Draw actual golden spiral
            spiral_angles = np.linspace(0, 4 * np.pi, 100)
            spiral_x = []
            spiral_y = []
            
            for sp_angle in spiral_angles:
                spiral_r = 3 * np.exp(sp_angle / (2 * np.pi)) * growth_stage
                if spiral_r < r_base:
                    sx = cx + spiral_r * np.cos(sp_angle)
                    sy = cy + spiral_r * np.sin(sp_angle)
                    spiral_x.append(sx)
                    spiral_y.append(sy)
            
            if len(spiral_x) > 1:
                ax.plot(spiral_x, spiral_y, 'k-', linewidth=0.4, alpha=0.4)
        
        # Add Fibonacci rectangle construction lines
        if i == n_circles // 2:  # Middle circle
            # Draw golden rectangles
            rect_size = r_base / 3
            for rect_idx in range(4):
                rect_angle = rect_idx * np.pi / 2
                
                # Rectangle corners based on golden ratio
                w = rect_size
                h = rect_size / phi
                
                corners = np.array([
                    [-w/2, -h/2], [w/2, -h/2], [w/2, h/2], [-w/2, h/2], [-w/2, -h/2]
                ])
                
                # Rotate rectangle
                cos_a, sin_a = np.cos(rect_angle), np.sin(rect_angle)
                rot_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
                rotated_corners = np.dot(corners, rot_matrix.T)
                
                # Translate to position
                rect_center = np.array([cx + r_base * 0.3 * np.cos(rect_angle), 
                                       cy + r_base * 0.3 * np.sin(rect_angle)])
                final_corners = rotated_corners + rect_center
                
                ax.plot(final_corners[:, 0], final_corners[:, 1], 'k-', linewidth=0.3, alpha=0.3)
    
    save(fig, "abstract concentric fibonacci spiral golden ratio organic pattern black white texture")

if __name__ == "__main__":
    draw()