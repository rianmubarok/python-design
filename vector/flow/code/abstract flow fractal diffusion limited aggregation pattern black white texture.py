import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def draw():
    """Diffusion-Limited Aggregation creating fractal branching patterns."""
    fig, ax = setup_ax()
    
    n_lines = 2200
    steps = 180
    step_size = 0.35
    
    # Seed points for aggregation
    seed_points = [(25, 25), (75, 25), (25, 75), (75, 75)]
    aggregated_points = set(seed_points)
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        # Start from random position
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for step in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Random walk (Brownian motion)
            dx = np.random.normal(0, 1)
            dy = np.random.normal(0, 1)
            
            # Bias toward aggregated regions
            min_dist_to_agg = float('inf')
            closest_agg = None
            
            for ax_pt, ay_pt in list(aggregated_points)[:100]:  # Limit for performance
                dist = np.sqrt((x - ax_pt)**2 + (y - ay_pt)**2)
                if dist < min_dist_to_agg:
                    min_dist_to_agg = dist
                    closest_agg = (ax_pt, ay_pt)
            
            if closest_agg and min_dist_to_agg < 20:
                # Attraction to aggregated structure
                attraction_strength = (20 - min_dist_to_agg) / 20 * 0.3
                dx += (closest_agg[0] - x) * attraction_strength
                dy += (closest_agg[1] - y) * attraction_strength
                
                # Stick if very close
                if min_dist_to_agg < 2:
                    aggregated_points.add((int(x), int(y)))
                    break
            
            # Add some deterministic flow patterns
            # Radial flow from center
            center_x, center_y = 50, 50
            r_center = np.sqrt((x - center_x)**2 + (y - center_y)**2) + 0.1
            
            if r_center > 30:  # Far from center, flow inward
                dx += -(x - center_x) * 0.02
                dy += -(y - center_y) * 0.02
            
            # Spiral component for interesting patterns
            angle = np.arctan2(y - center_y, x - center_x)
            spiral_strength = 0.1
            dx += -spiral_strength * np.sin(angle)
            dy += spiral_strength * np.cos(angle)
            
            # Scale factor based on density
            local_density = len([p for p in aggregated_points 
                               if np.sqrt((x - p[0])**2 + (y - p[1])**2) < 10])
            density_factor = 1.0 / (1.0 + local_density * 0.1)
            
            dx *= density_factor
            dy *= density_factor
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.2, linewidth=0.7)
            
    save(fig, "abstract flow fractal diffusion limited aggregation pattern black white texture")


if __name__ == "__main__":
    draw()