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
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
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
    """Generates Moire interference using concentric circles."""
    fig, ax = setup_ax()
    
    radii = np.linspace(0.01, 2.5, 120)
    theta = np.linspace(0, 2*np.pi, 500)
    
    # First set of concentric circles
    center1_x, center1_y = -0.05, -0.05
    for r in radii:
        x = center1_x + r * np.cos(theta)
        y = center1_y + r * np.sin(theta)
        ax.plot(x, y, color="black", linewidth=1.0)
        
    # Second set of concentric circles (slightly offset)
    center2_x, center2_y = 0.05, 0.05
    for r in radii:
        x = center2_x + r * np.cos(theta)
        y = center2_y + r * np.sin(theta)
        ax.plot(x, y, color="black", linewidth=1.0)

    save(fig, "abstract opart moire interference waves kinetic pattern black white texture")

if __name__ == "__main__":
    generate()
