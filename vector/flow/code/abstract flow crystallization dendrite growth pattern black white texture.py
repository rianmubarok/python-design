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
    """Flow simulating crystal dendrite growth patterns."""
    fig, ax = setup_ax()
    
    n_lines = 1800
    steps = 180
    step_size = 0.35
    
    # Crystal nucleation sites
    crystal_centers = [(25, 25), (75, 25), (25, 75), (75, 75), (50, 50)]
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for step in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            dx, dy = 0, 0
            
            # Growth from crystal centers
            for cx, cy in crystal_centers:
                dist = np.sqrt((x - cx)**2 + (y - cy)**2) + 0.1
                
                # Diffusion-limited aggregation
                if dist < 30:  # Within growth zone
                    # Preferential growth along crystallographic axes
                    angle_to_center = np.arctan2(y - cy, x - cx)
                    
                    # 6-fold symmetry (hexagonal crystal)
                    preferred_angles = [i * np.pi / 3 for i in range(6)]
                    angle_forces = []
                    
                    for pref_angle in preferred_angles:
                        angle_diff = abs(angle_to_center - pref_angle)
                        angle_diff = min(angle_diff, 2*np.pi - angle_diff)
                        force = np.exp(-angle_diff * 3) * (30 - dist) / 30
                        
                        force_x = force * np.cos(pref_angle) * 0.1
                        force_y = force * np.sin(pref_angle) * 0.1
                        
                        dx += force_x
                        dy += force_y
            
            # Supersaturation gradient
            supersaturation = np.sin(x * 0.1) * np.cos(y * 0.1) + 1
            dx *= supersaturation
            dy *= supersaturation
            
            # Thermal fluctuations
            temperature_noise = 0.3
            dx += np.random.normal(0, temperature_noise)
            dy += np.random.normal(0, temperature_noise)
            
            # Branching instability
            if step % 20 == 0:  # Periodic branching
                branch_angle = np.random.uniform(0, 2*np.pi)
                branch_strength = 0.5
                dx += branch_strength * np.cos(branch_angle)
                dy += branch_strength * np.sin(branch_angle)
            
            # Surface tension effects (smoothing)
            dx += 0.1 * np.sin(x * 0.4 + y * 0.3)
            dy += 0.1 * np.cos(x * 0.3 + y * 0.4)
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.3, linewidth=0.7)
            
    save(fig, "abstract flow crystallization dendrite growth pattern black white texture")


if __name__ == "__main__":
    draw()