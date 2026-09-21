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


def seamless_noise(x, y, frequency):
    """Generate seamless Perlin-like noise using trigonometric interpolation."""
    # Convert to [0, 2π] for seamless tiling
    sx = (x / 100) * 2 * np.pi * frequency
    sy = (y / 100) * 2 * np.pi * frequency
    
    # Multi-dimensional noise using trigonometric functions
    n1 = np.sin(sx) * np.cos(sy)
    n2 = np.cos(sx) * np.sin(sy)  
    n3 = np.sin(sx + sy) * 0.5
    n4 = np.cos(sx - sy) * 0.3
    
    return n1 + n2 + n3 + n4


def draw():
    """Multi-octave seamless turbulence using Perlin-like noise."""
    fig, ax = setup_ax()
    
    n_lines = 2500
    steps = 160
    step_size = 0.3
    
    # Octave parameters
    octaves = [1, 2, 4, 8]
    amplitudes = [1.0, 0.5, 0.25, 0.125]
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for _ in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            dx, dy = 0, 0
            
            # Sum multiple octaves
            for octave, amplitude in zip(octaves, amplitudes):
                # Noise values at current position
                noise_x = seamless_noise(x, y, octave) * amplitude
                noise_y = seamless_noise(x + 47.3, y + 23.7, octave) * amplitude  # Offset for independence
                
                # Gradient estimation (for flow direction)
                epsilon = 0.5
                grad_x = (seamless_noise(x + epsilon, y, octave) - 
                         seamless_noise(x - epsilon, y, octave)) / (2 * epsilon) * amplitude
                grad_y = (seamless_noise(x, y + epsilon, octave) - 
                         seamless_noise(x, y - epsilon, octave)) / (2 * epsilon) * amplitude
                
                # Flow perpendicular to gradient (curl)
                dx += -grad_y
                dy += grad_x
                
                # Direct noise contribution
                dx += noise_x * 0.2
                dy += noise_y * 0.2
            
            # Normalize and apply step
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            # Seamless wrapping
            x = x % 100
            y = y % 100
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.18, linewidth=0.8)
            
    save(fig, "abstract flow seamless perlin turbulence octave pattern black white texture")


if __name__ == "__main__":
    draw()