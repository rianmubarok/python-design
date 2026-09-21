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
    Plasma Electromagnetic Storm Aurora Pattern.
    Concentric circles representing aurora patterns with plasma instabilities,
    electromagnetic field lines, and solar wind interactions.
    """
    fig, ax = setup_ax()
    
    cx, cy = 50.0, 50.0
    n_circles = 40
    max_radius = 72.0
    n_pts = 600
    
    # Plasma parameters
    solar_wind_velocity = np.array([0.3, -0.1])  # Solar wind direction
    magnetic_field_lines = [
        {"angle": 0, "strength": 1.0},      # Horizontal field
        {"angle": np.pi/6, "strength": 0.7}, # Diagonal field  
        {"angle": -np.pi/4, "strength": 0.5} # Another diagonal
    ]
    
    # Aurora emission altitudes (different layers)
    emission_layers = [0.3, 0.5, 0.7, 0.85]  # Normalized altitudes
    
    for i in range(1, n_circles + 1):
        altitude_factor = i / n_circles
        r_base = max_radius * altitude_factor ** 1.3
        
        # Determine which emission layer this circle belongs to
        current_layer = 0
        for j, layer_alt in enumerate(emission_layers):
            if altitude_factor <= layer_alt:
                current_layer = j
                break
        
        angles = np.linspace(0, 2 * np.pi, n_pts)
        x_pts = []
        y_pts = []
        
        for angle in angles:
            x_base = r_base * np.cos(angle)
            y_base = r_base * np.sin(angle)
            current_pos = np.array([cx + x_base, cy + y_base])
            
            # Plasma instabilities (Kelvin-Helmholtz, Rayleigh-Taylor)
            kh_instability = 0.2 * np.sin(angle * 8 + altitude_factor * 4 * np.pi) * \
                           np.exp(-altitude_factor * 2)
            rt_instability = 0.15 * np.sin(angle * 12 + altitude_factor * 6 * np.pi) * \
                           altitude_factor
            
            # Electromagnetic field line following
            field_modulation = 0
            for field in magnetic_field_lines:
                # Calculate field line curvature
                field_direction = np.array([np.cos(field["angle"]), np.sin(field["angle"])])
                position_along_field = np.dot(current_pos - np.array([cx, cy]), field_direction)
                
                # Field line oscillation (due to plasma waves)
                field_wave = field["strength"] * np.sin(position_along_field * 0.3 + 
                                                       altitude_factor * 2 * np.pi)
                field_modulation += 0.1 * field_wave
            
            # Solar wind interaction (bow shock effects)
            wind_interaction = np.dot(solar_wind_velocity, 
                                    (current_pos - np.array([cx, cy])) / np.linalg.norm(current_pos - np.array([cx, cy])))
            shock_modulation = 0.12 * np.tanh(wind_interaction * 3) * altitude_factor
            
            # Particle precipitation patterns (aurora curtains)
            precipitation_angle = angle + altitude_factor * np.pi
            curtain_pattern = 0.18 * np.sin(precipitation_angle * 6) * \
                            np.cos(precipitation_angle * 3) * \
                            np.exp(-abs(angle - np.pi) * 2)  # Concentration near midnight
            
            # Electromagnetic wave propagation (Alfvén waves)
            alfven_frequency = 0.5 + 0.3 * current_layer  # Different frequencies per layer
            alfven_wave = 0.08 * np.sin(angle * 10 + altitude_factor * alfven_frequency * 8 * np.pi)
            
            # Plasma density fluctuations
            density_fluctuation = 0.1 * np.sin(angle * 15 + altitude_factor * 3 * np.pi) * \
                                np.cos(angle * 7)
            
            # Combine all plasma effects
            total_plasma_effect = (kh_instability + rt_instability + field_modulation + 
                                 shock_modulation + curtain_pattern + alfven_wave + 
                                 density_fluctuation)
            
            # Apply aurora morphology
            radius_final = r_base * (1 + total_plasma_effect)
            
            x_final = cx + radius_final * np.cos(angle)
            y_final = cy + radius_final * np.sin(angle)
            
            x_pts.append(x_final)
            y_pts.append(y_final)
        
        # Close the aurora loop
        x_pts.append(x_pts[0])
        y_pts.append(y_pts[0])
        
        # Line width varies with plasma activity and emission intensity
        plasma_activity = abs(kh_instability) + abs(rt_instability) + abs(curtain_pattern)
        lw = 0.4 + 1.2 * min(plasma_activity * 3, 1.5)
        
        # Different alpha for different emission layers
        layer_alpha = 0.6 + 0.4 * (current_layer / len(emission_layers))
        
        ax.plot(x_pts, y_pts, 'k-', linewidth=lw, alpha=layer_alpha)
        
        # Add magnetic field lines (every 6th circle)
        if i % 6 == 0 and i > 12:
            for field in magnetic_field_lines:
                if field["strength"] > 0.6:  # Only draw strong field lines
                    # Field line from center outward
                    field_length = r_base * 0.8
                    x1 = cx + (field_length * 0.2) * np.cos(field["angle"])
                    y1 = cy + (field_length * 0.2) * np.sin(field["angle"])
                    x2 = cx + field_length * np.cos(field["angle"])
                    y2 = cy + field_length * np.sin(field["angle"])
                    
                    # Add field line curvature
                    n_segments = 10
                    field_x = np.linspace(x1, x2, n_segments)
                    field_y = np.linspace(y1, y2, n_segments)
                    
                    # Apply plasma wave modulation to field line
                    for j in range(n_segments):
                        wave_mod = 0.5 * np.sin(j * 0.8 + altitude_factor * 2 * np.pi)
                        perpendicular = np.array([-np.sin(field["angle"]), np.cos(field["angle"])])
                        field_x[j] += wave_mod * perpendicular[0]
                        field_y[j] += wave_mod * perpendicular[1]
                    
                    ax.plot(field_x, field_y, 'k-', linewidth=0.4, alpha=0.5)
    
    save(fig, "abstract concentric plasma electromagnetic storm aurora pattern black white texture")

if __name__ == "__main__":
    draw()