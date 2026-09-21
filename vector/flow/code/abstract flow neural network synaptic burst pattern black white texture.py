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
    """Neural network-like flow with synaptic bursts and dendrite patterns."""
    fig, ax = setup_ax()
    
    n_lines = 1500
    steps = 150
    step_size = 0.5
    
    # Create neural nodes
    n_nodes = 25
    nodes = [(np.random.uniform(10, 90), np.random.uniform(10, 90)) for _ in range(n_nodes)]
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for step in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            dx, dy = 0, 0
            
            # Attraction/repulsion from neural nodes
            for nx, ny in nodes:
                dist = np.sqrt((x - nx)**2 + (y - ny)**2) + 0.1
                
                # Synaptic burst effect - periodic activation
                activation = np.sin(step * 0.1 + nx * 0.1 + ny * 0.1) > 0.3
                
                if activation and dist < 15:  # Within synaptic range
                    # Strong directional flow during burst
                    force = 8.0 / (dist + 1)
                    dx += (nx - x) * force / dist
                    dy += (ny - y) * force / dist
                else:
                    # Weak repulsion when inactive
                    force = 0.5 / (dist + 1)
                    dx -= (nx - x) * force / dist
                    dy -= (ny - y) * force / dist
            
            # Add dendritic branching noise
            dx += np.sin(x * 0.3 + step * 0.05) * 0.8
            dy += np.cos(y * 0.3 + step * 0.05) * 0.8
            
            # Neural oscillation patterns
            dx += 0.3 * np.sin(x * 0.15 + y * 0.1 + step * 0.02)
            dy += 0.3 * np.cos(x * 0.1 + y * 0.15 + step * 0.02)
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.3, linewidth=0.9)
            
    save(fig, "abstract flow neural network synaptic burst pattern black white texture")


if __name__ == "__main__":
    draw()