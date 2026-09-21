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
    """Flow based on Fibonacci spiral and golden ratio proportions."""
    fig, ax = setup_ax()
    
    n_lines = 2000
    steps = 200
    step_size = 0.3
    
    # Golden ratio and related constants
    phi = (1 + np.sqrt(5)) / 2  # Golden ratio
    center_x, center_y = 50, 50
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for step in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Distance and angle from center
            r = np.sqrt((x - center_x)**2 + (y - center_y)**2) + 0.1
            theta = np.arctan2(y - center_y, x - center_x)
            
            # Fibonacci spiral parameters
            # r = a * e^(b*theta) where b = 2/phi for golden spiral
            spiral_b = 2 / phi
            
            # Target spiral radius for current angle
            target_r = 10 * np.exp(spiral_b * (theta + step * 0.02))
            
            # Radial flow toward/away from spiral
            radial_force = (target_r - r) * 0.02
            
            # Tangential flow along spiral
            tangential_velocity = r * 0.05
            
            # Convert to Cartesian
            dx = np.cos(theta) * radial_force - np.sin(theta) * tangential_velocity
            dy = np.sin(theta) * radial_force + np.cos(theta) * tangential_velocity
            
            # Add golden ratio harmonics
            dx += 0.2 * np.sin(theta * phi + step * 0.01)
            dy += 0.2 * np.cos(theta * phi + step * 0.01)
            
            # Fibonacci sequence perturbations
            fib_n = int(step / 10) % 8
            fib_sequence = [1, 1, 2, 3, 5, 8, 13, 21]
            fib_freq = fib_sequence[fib_n] * 0.1
            
            dx += 0.1 * np.sin(r * fib_freq)
            dy += 0.1 * np.cos(r * fib_freq)
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.2, linewidth=0.8)
            
    save(fig, "abstract flow fibonacci spiral golden ratio stream pattern black white texture")


if __name__ == "__main__":
    draw()