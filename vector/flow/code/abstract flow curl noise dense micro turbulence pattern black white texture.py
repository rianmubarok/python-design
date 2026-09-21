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
    """Dense micro-scale turbulent flow with much smaller step size and more particles."""
    fig, ax = setup_ax()
    
    n_lines = 5000  # Increased density
    steps = 300  # More steps
    step_size = 0.15  # Much smaller steps for micro detail
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for _ in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Higher frequency curl noise for micro turbulence
            dx = np.sin(y * 0.25) + 0.8 * np.cos(y * 0.4) - 0.6 * np.sin(x * 0.6)
            dy = np.cos(x * 0.25) - 0.8 * np.sin(x * 0.4) + 0.6 * np.cos(y * 0.6)
            
            # Add micro-scale noise
            dx += 0.3 * np.sin(x * 1.2 + y * 0.8)
            dy += 0.3 * np.cos(y * 1.2 + x * 0.8)
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.15, linewidth=0.6)
            
    save(fig, "abstract flow curl noise dense micro turbulence pattern black white texture")


if __name__ == "__main__":
    draw()