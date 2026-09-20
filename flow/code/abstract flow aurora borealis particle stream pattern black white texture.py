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
    """Charged particles flowing along Earth's magnetic field lines (aurora)."""
    fig, ax = setup_ax()
    
    n_lines = 1500
    steps = 200
    step_size = 0.3
    
    # Magnetic dipole (Earth's center)
    mag_center_x, mag_center_y = 50, 40
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        # Start particles from "solar wind" (top of canvas)
        x = np.random.uniform(20, 80)
        y = np.random.uniform(80, 95)
        
        for step in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Distance from magnetic center
            r = np.sqrt((x - mag_center_x)**2 + (y - mag_center_y)**2) + 0.1
            theta = np.arctan2(y - mag_center_y, x - mag_center_x)
            
            # Dipole magnetic field
            # B_r = 2*cos(theta)/r^3, B_theta = sin(theta)/r^3
            B_r = 2 * np.cos(theta - np.pi/2) / (r**2)  # Adjust for coordinate system
            B_theta = np.sin(theta - np.pi/2) / (r**2)
            
            # Convert to Cartesian
            B_x = B_r * np.cos(theta) - B_theta * np.sin(theta)
            B_y = B_r * np.sin(theta) + B_theta * np.cos(theta)
            
            # Particle motion along field lines
            field_strength = 10.0
            dx = B_x * field_strength
            dy = B_y * field_strength
            
            # Spiral motion due to Lorentz force
            cyclotron_freq = 0.1
            spiral_radius = 2.0
            
            # Add cyclotron motion perpendicular to field
            perp_x = -B_y  # Perpendicular to field
            perp_y = B_x
            perp_mag = np.sqrt(perp_x**2 + perp_y**2) + 0.0001
            perp_x /= perp_mag
            perp_y /= perp_mag
            
            cyclotron_x = perp_x * np.sin(step * cyclotron_freq) * spiral_radius
            cyclotron_y = perp_y * np.sin(step * cyclotron_freq) * spiral_radius
            
            dx += cyclotron_x * 0.1
            dy += cyclotron_y * 0.1
            
            # Atmospheric interaction (precipitation)
            if y < 50:  # Lower atmosphere
                precipitation_strength = (50 - y) / 50
                dx *= (1 - precipitation_strength * 0.8)
                dy *= (1 - precipitation_strength * 0.8)
                
                # Random scattering in atmosphere
                dx += np.random.normal(0, precipitation_strength * 0.5)
                dy += np.random.normal(0, precipitation_strength * 0.3)
            
            # Solar wind pressure
            if y > 70:
                solar_pressure = 0.3
                dy -= solar_pressure
            
            # Magnetosphere compression/stretching
            if x < 30 or x > 70:  # Magnetotail effects
                tail_stretch = 0.2
                dx += (50 - x) * tail_stretch * 0.01
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.25, linewidth=0.7)
            
    save(fig, "abstract flow aurora borealis particle stream pattern black white texture")


if __name__ == "__main__":
    draw()