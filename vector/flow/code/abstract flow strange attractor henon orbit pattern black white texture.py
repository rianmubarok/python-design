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
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.5, 0.5)
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
    """Henon Attractor with variations in parameters for different orbit patterns."""
    fig, ax = setup_ax()
    
    # Henon Attractor parameters
    a, b = 1.4, 0.3
    
    n_points = 200000
    x, y = np.zeros(n_points), np.zeros(n_points)
    
    # Multiple starting points for denser pattern
    for start_idx in range(0, n_points, 25000):
        if start_idx + 25000 > n_points:
            break
            
        # Slightly different starting conditions
        x[start_idx] = np.random.uniform(-0.1, 0.1)
        y[start_idx] = np.random.uniform(-0.1, 0.1)
        
        for i in range(start_idx + 1, min(start_idx + 25000, n_points)):
            x[i] = 1 - a * x[i-1]**2 + y[i-1]
            y[i] = b * x[i-1]
    
    # Plot with varying transparency for depth effect
    ax.scatter(x[:50000], y[:50000], s=0.1, c="black", alpha=0.15)
    ax.scatter(x[50000:100000], y[50000:100000], s=0.1, c="black", alpha=0.1)
    ax.scatter(x[100000:150000], y[100000:150000], s=0.1, c="black", alpha=0.08)
    ax.scatter(x[150000:], y[150000:], s=0.1, c="black", alpha=0.05)
    
    save(fig, "abstract flow strange attractor henon orbit pattern black white texture")


if __name__ == "__main__":
    draw()