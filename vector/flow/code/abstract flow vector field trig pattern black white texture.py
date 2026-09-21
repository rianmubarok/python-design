import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 100
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


def abstract_flow_vector_field_trig_pattern_black_white_texture():
    """Generates a vector field flow using trigonometric functions to simulate turbulence."""
    fig, ax = setup_ax()
    
    n_lines = 1500
    steps = 100
    step_size = 0.5
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        # Random starting point
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for _ in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Vector field based on sin/cos
            angle = np.sin(x * 0.05) * np.cos(y * 0.05) * np.pi * 2 + np.sin(x * 0.1) * np.pi
            
            x += np.cos(angle) * step_size
            y += np.sin(angle) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.3, linewidth=0.8)
            
    save(fig, "abstract flow vector field trig pattern black white texture")


if __name__ == "__main__":
    abstract_flow_vector_field_trig_pattern_black_white_texture()
