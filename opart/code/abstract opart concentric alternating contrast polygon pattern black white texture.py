import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
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
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
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
    """Generates a high-contrast alternating concentric polygon op-art."""
    fig, ax = setup_ax()
    
    n_polys = 60
    base_radius = 15.0
    
    for i in range(n_polys):
        r = base_radius * (1 - i / n_polys)**1.5
        color = "black" if i % 2 == 0 else "white"
        edgecolor = "black"
        linewidth = 0.5 if color == "white" else 0.0
        
        # alternating between two shapes (e.g., octagon and square)
        # to create more dynamic dazzle effect
        vertices = 8 if i % 4 < 2 else 12
        angle = 0 if i % 4 < 2 else np.pi / 12
        
        poly = RegularPolygon((0, 0), numVertices=vertices, radius=r, orientation=angle, 
                              facecolor=color, edgecolor=edgecolor, linewidth=linewidth)
        ax.add_patch(poly)

    save(fig, "abstract opart concentric alternating contrast polygon pattern black white texture")

if __name__ == "__main__":
    generate()
