import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
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


def draw():
    """
    Retro Halftone Dot Print.
    A rigid grid of dots whose radii vary based on a mathematical
    interference formula, simulating a retro newspaper halftone print.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches
    
    n_dots = 80
    spacing = 120.0 / n_dots
    
    for row in range(-2, n_dots + 2):
        for col in range(-2, n_dots + 2):
            cx = -10 + col * spacing
            cy = -10 + row * spacing
            
            # Mathematical interference function for the "image"
            # We use a combination of radial ripples and horizontal waves
            dist1 = np.sqrt((cx - 30)**2 + (cy - 70)**2)
            dist2 = np.sqrt((cx - 80)**2 + (cy - 20)**2)
            
            val = np.sin(dist1 * 0.2) + np.cos(dist2 * 0.15) + np.sin(cx * 0.1) * np.cos(cy * 0.1)
            
            # Normalize to [0, 1]
            val = (val + 3.0) / 6.0
            
            # Use value to determine dot radius
            max_r = spacing * 0.65
            r = val * max_r
            
            if r > 0.1:
                # To simulate printing errors, occasionally offset slightly
                jitter_x = np.random.uniform(-0.1, 0.1) * spacing
                jitter_y = np.random.uniform(-0.1, 0.1) * spacing
                
                circle = patches.Circle((cx + jitter_x, cy + jitter_y), r, 
                                        facecolor='black', edgecolor='none')
                ax.add_patch(circle)

    save(fig, "abstract grid tessellation retro halftone dot print scaling pattern black white texture")


if __name__ == "__main__":
    draw()
