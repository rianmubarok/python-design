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
    """Galactic spiral density waves like in spiral galaxies."""
    fig, ax = setup_ax()
    
    n_lines = 2200
    steps = 180
    step_size = 0.35
    
    center_x, center_y = 50, 50
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for _ in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Distance and angle from center
            r = np.sqrt((x - center_x)**2 + (y - center_y)**2) + 0.1
            theta = np.arctan2(y - center_y, x - center_x)
            
            # Differential rotation (like galaxy)
            omega = 0.1 / (r * 0.1 + 1)  # Angular velocity decreases with radius
            
            # Spiral density wave pattern
            spiral_angle = theta + np.log(r * 0.1 + 1) * 0.8  # Logarithmic spiral
            wave_strength = np.sin(2 * spiral_angle) * np.exp(-r * 0.02)
            
            # Tangential velocity (rotation)
            vx_rot = -(y - center_y) * omega
            vy_rot = (x - center_x) * omega
            
            # Radial perturbation from density wave
            vx_wave = np.cos(theta) * wave_strength * 0.5
            vy_wave = np.sin(theta) * wave_strength * 0.5
            
            # Combine velocities
            dx = vx_rot + vx_wave
            dy = vy_rot + vy_wave
            
            # Add turbulence
            dx += 0.1 * np.sin(x * 0.2 + y * 0.15)
            dy += 0.1 * np.cos(x * 0.15 + y * 0.2)
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.25, linewidth=0.7)
            
    save(fig, "abstract flow galaxy spiral arms density wave pattern black white texture")


if __name__ == "__main__":
    draw()