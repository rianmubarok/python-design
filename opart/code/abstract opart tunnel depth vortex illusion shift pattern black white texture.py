import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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
    ax.set_xlim(-60, 60)
    ax.set_ylim(-60, 60)
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

def generate():
    """Generates an off-center twisting spiral vortex tunnel."""
    fig, ax = setup_ax()
    
    n_steps = 150
    size = 55.0
    angle = 0.0
    center_x = 0.0
    center_y = 0.0
    
    for i in range(n_steps):
        if size <= 0.2:
            break
            
        square = np.array([
            [-size, -size],
            [size, -size],
            [size, size],
            [-size, size]
        ])
        
        rot_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        
        rotated_square = square @ rot_matrix.T
        
        # Shift center towards bottom right
        rotated_square[:, 0] += center_x
        rotated_square[:, 1] += center_y
        
        poly = Polygon(rotated_square, fill=False, edgecolor="black", linewidth=0.3 + 1.0 * (i / n_steps))
        ax.add_patch(poly)
        
        size *= 0.96
        angle += 0.05
        center_x += 0.3
        center_y -= 0.2

    save(fig, "abstract opart tunnel depth vortex illusion shift pattern black white texture")

if __name__ == "__main__":
    generate()
