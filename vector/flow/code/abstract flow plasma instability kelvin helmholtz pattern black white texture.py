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
    """Kelvin-Helmholtz instability - when two fluids flow past each other."""
    fig, ax = setup_ax()
    
    n_lines = 2500
    steps = 150
    step_size = 0.4
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for step in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Base shear flow (different velocities at different heights)
            if y < 50:
                base_velocity = 1.0  # Lower layer moves right
            else:
                base_velocity = -0.5  # Upper layer moves left
            
            # Kelvin-Helmholtz instability grows near interface
            interface_distance = abs(y - 50)
            instability_strength = np.exp(-interface_distance / 10) * (step * 0.01)
            
            # Growing wavelike perturbations
            wave_x = np.sin(x * 0.2 + step * 0.05) * instability_strength
            wave_y = np.cos(x * 0.15 + step * 0.03) * instability_strength * 0.5
            
            # Vorticity generation at interface
            vorticity = np.exp(-interface_distance / 8) * np.sin(x * 0.1 + step * 0.02)
            
            dx = base_velocity + wave_x + vorticity * 0.3
            dy = wave_y + vorticity * -(y - 50) * 0.05
            
            # Add turbulent mixing
            if interface_distance < 15:
                mixing_x = np.random.normal(0, 0.5) * (15 - interface_distance) / 15
                mixing_y = np.random.normal(0, 0.3) * (15 - interface_distance) / 15
                dx += mixing_x
                dy += mixing_y
            
            # Non-linear effects
            dx += 0.1 * np.sin(y * 0.3 + x * 0.1)
            dy += 0.1 * np.cos(x * 0.2 + y * 0.15)
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.25, linewidth=0.8)
            
    save(fig, "abstract flow plasma instability kelvin helmholtz pattern black white texture")


if __name__ == "__main__":
    draw()