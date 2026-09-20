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
    """Macro-scale wide swirls with larger step size for broader flow patterns."""
    fig, ax = setup_ax()
    
    n_lines = 800  # Fewer lines for macro effect
    steps = 80  # Fewer steps
    step_size = 1.2  # Much larger steps for macro patterns
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for _ in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Lower frequency for macro swirls
            dx = np.sin(y * 0.02) + 0.7 * np.cos(y * 0.035) - 0.4 * np.sin(x * 0.025)
            dy = np.cos(x * 0.02) - 0.7 * np.sin(x * 0.035) + 0.4 * np.cos(y * 0.025)
            
            # Add large-scale vorticity
            cx, cy = 50, 50  # Center of main vortex
            vx = -(y - cy) * 0.01
            vy = (x - cx) * 0.01
            
            dx += vx
            dy += vy
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.4, linewidth=1.5)
            
    save(fig, "abstract flow curl noise macro wide swirl pattern black white texture")


if __name__ == "__main__":
    draw()