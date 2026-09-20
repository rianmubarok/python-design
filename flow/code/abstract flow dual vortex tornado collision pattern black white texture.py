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
    """Two counter-rotating vortices colliding and interfering with each other."""
    fig, ax = setup_ax()
    
    n_lines = 2500
    steps = 200
    step_size = 0.3
    
    # Two vortex centers
    vortex1_x, vortex1_y = 25, 50
    vortex2_x, vortex2_y = 75, 50
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for _ in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # First vortex (clockwise)
            r1 = np.sqrt((x - vortex1_x)**2 + (y - vortex1_y)**2) + 0.1
            angle1 = np.arctan2(y - vortex1_y, x - vortex1_x)
            strength1 = 15.0 / r1
            vx1 = -strength1 * np.sin(angle1)
            vy1 = strength1 * np.cos(angle1)
            
            # Second vortex (counter-clockwise)
            r2 = np.sqrt((x - vortex2_x)**2 + (y - vortex2_y)**2) + 0.1
            angle2 = np.arctan2(y - vortex2_y, x - vortex2_x)
            strength2 = 15.0 / r2
            vx2 = strength2 * np.sin(angle2)
            vy2 = -strength2 * np.cos(angle2)
            
            # Combine vortices
            dx = vx1 + vx2
            dy = vy1 + vy2
            
            # Add turbulence at collision zone
            collision_zone = np.exp(-((x-50)**2 + (y-50)**2) / 400)
            turbulence_x = collision_zone * np.sin(x * 0.3 + y * 0.2) * 2
            turbulence_y = collision_zone * np.cos(x * 0.2 + y * 0.3) * 2
            
            dx += turbulence_x
            dy += turbulence_y
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.3, linewidth=0.8)
            
    save(fig, "abstract flow dual vortex tornado collision pattern black white texture")


if __name__ == "__main__":
    draw()