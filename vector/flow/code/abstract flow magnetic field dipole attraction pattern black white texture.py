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
    """Magnetic dipole field lines flowing from north to south pole."""
    fig, ax = setup_ax()
    
    n_lines = 1800
    steps = 250
    step_size = 0.2
    
    # Dipole positions
    north_pole = (50, 25)
    south_pole = (50, 75)
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for _ in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Distance to poles
            rn = np.sqrt((x - north_pole[0])**2 + (y - north_pole[1])**2) + 0.1
            rs = np.sqrt((x - south_pole[0])**2 + (y - south_pole[1])**2) + 0.1
            
            # Magnetic field from north pole (repulsive)
            fn_x = (x - north_pole[0]) / rn**3
            fn_y = (y - north_pole[1]) / rn**3
            
            # Magnetic field from south pole (attractive)
            fs_x = -(x - south_pole[0]) / rs**3
            fs_y = -(y - south_pole[1]) / rs**3
            
            # Combine fields
            dx = fn_x + fs_x
            dy = fn_y + fs_y
            
            # Scale field strength
            dx *= 30
            dy *= 30
            
            # Add slight curl for more organic flow
            curl_strength = 0.1
            dx += curl_strength * np.sin(y * 0.1)
            dy += curl_strength * np.cos(x * 0.1)
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.25, linewidth=0.9)
            
    save(fig, "abstract flow magnetic field dipole attraction pattern black white texture")


if __name__ == "__main__":
    draw()