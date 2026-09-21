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
    Neural Network Synaptic Firing Pattern.
    Concentric circles modulated by neural firing patterns with
    synaptic connections, action potentials, and neural plasticity effects.
    """
    fig, ax = setup_ax()
    
    cx, cy = 50.0, 50.0
    n_layers = 35
    max_radius = 68.0
    n_pts = 500
    
    # Neural network parameters
    firing_nodes = np.random.rand(20) * 2 * np.pi  # Random firing neuron positions
    firing_strengths = np.random.rand(20) * 0.8 + 0.2  # Firing intensities
    synapse_delays = np.random.rand(20) * np.pi  # Temporal delays
    
    for i in range(1, n_layers + 1):
        layer_depth = i / n_layers
        r_base = max_radius * layer_depth ** 1.3
        
        angles = np.linspace(0, 2 * np.pi, n_pts)
        x_pts = []
        y_pts = []
        
        for angle in angles:
            # Calculate neural activation at this point
            total_activation = 0
            
            for node_angle, strength, delay in zip(firing_nodes, firing_strengths, synapse_delays):
                # Distance-based activation (neural influence radius)
                angle_diff = min(abs(angle - node_angle), 2*np.pi - abs(angle - node_angle))
                spatial_influence = np.exp(-angle_diff * 3)  # Gaussian spatial influence
                
                # Temporal firing pattern (action potential shape)
                temporal_pattern = np.sin(r_base * 0.5 + delay) * np.exp(-r_base * 0.1)
                
                # Synaptic strength modulation
                synapse_modulation = strength * spatial_influence * temporal_pattern
                total_activation += synapse_modulation
            
            # Neural plasticity effects (Hebbian learning-like modulation)
            plasticity = 0.1 * np.sin(angle * 7 + r_base * 0.3) * np.cos(angle * 3)
            
            # Action potential propagation (directional bias)
            propagation = 0.08 * np.sin(angle * 2 + r_base * 0.8) * layer_depth
            
            # Final radius with neural modulation
            neural_modulation = 0.25 * total_activation + plasticity + propagation
            radius_final = r_base * (1 + neural_modulation)
            
            x = cx + radius_final * np.cos(angle)
            y = cy + radius_final * np.sin(angle)
            
            x_pts.append(x)
            y_pts.append(y)
        
        # Close the neural layer
        x_pts.append(x_pts[0])
        y_pts.append(y_pts[0])
        
        # Line width based on layer activation level
        avg_activation = np.mean([strength for strength in firing_strengths])
        lw = 0.5 + 1.0 * avg_activation * layer_depth
        
        ax.plot(x_pts, y_pts, 'k-', linewidth=lw, alpha=0.8)
        
        # Add synaptic connections (sparse connections between layers)
        if i % 6 == 0 and i > 6:
            n_connections = int(8 * layer_depth)  # More connections in deeper layers
            for conn in range(n_connections):
                conn_angle = np.random.rand() * 2 * np.pi
                
                # Connection from previous layer
                r_prev = max_radius * ((i-3) / n_layers) ** 1.3
                x1 = cx + r_prev * np.cos(conn_angle)
                y1 = cy + r_prev * np.sin(conn_angle)
                
                # Connection to current layer with some angular variation
                angle_var = (np.random.rand() - 0.5) * 0.5
                x2 = cx + r_base * np.cos(conn_angle + angle_var)
                y2 = cy + r_base * np.sin(conn_angle + angle_var)
                
                # Draw synaptic connection
                ax.plot([x1, x2], [y1, y2], 'k-', linewidth=0.2, alpha=0.3)
    
    save(fig, "abstract concentric neural network synaptic firing pattern black white texture")

if __name__ == "__main__":
    draw()