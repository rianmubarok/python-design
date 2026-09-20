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
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
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


def nested_pentagon_starburst():
    """
    Geometric nested pentagons with starburst lines radiating from vertices.
    Each layer has progressively larger pentagons with rotation offset.
    """
    fig, ax = setup_ax()
    
    cx, cy = 50, 50
    n_layers = 15
    
    for i in range(n_layers):
        radius = 3 + i * 2.8
        rotation = i * 12  # Progressive rotation
        
        # Pentagon vertices
        angles = np.array([2 * np.pi * k / 5 + np.radians(rotation) for k in range(6)])  # 6 to close
        
        x_points = cx + radius * np.cos(angles)
        y_points = cy + radius * np.sin(angles)
        
        # Draw pentagon
        lw = 0.8 + 1.5 * (i / n_layers)
        ax.plot(x_points, y_points, color="black", linewidth=lw, solid_capstyle="round")
        
        # Draw starburst lines from vertices (every 3rd layer)
        if i % 3 == 0 and i > 0:
            for j in range(5):  # 5 vertices
                start_x = x_points[j]
                start_y = y_points[j]
                
                # Radiate outward from vertex
                line_length = radius * 0.4
                end_x = start_x + line_length * np.cos(angles[j])
                end_y = start_y + line_length * np.sin(angles[j])
                
                ax.plot([start_x, end_x], [start_y, end_y], 
                       color="black", linewidth=0.6, alpha=0.7)
    
    save(fig, "nested pentagon starburst")


if __name__ == "__main__":
    nested_pentagon_starburst()