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
EPS_DIR = OUTPUT_DIR / "eps"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


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
    eps_path = EPS_DIR / f"{name} {DATE}.eps"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    # Save EPS with larger figure size for 4MP+ bounding box
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format="eps", pad_inches=0, facecolor="white", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path} | {eps_path}")


def draw():
    """
    Geometric Octagon Morph Triangle Transition.
    Concentric shapes that morph from octagons at the center to triangles at the edge,
    creating a smooth geometric transition pattern.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_shapes = 40
    max_radius = 65.0
    
    for i in range(1, n_shapes + 1):
        r = max_radius * (i / n_shapes)
        
        # Morph factor: 0 (octagon) to 1 (triangle)
        morph_factor = (i - 1) / (n_shapes - 1)
        
        # Interpolate between octagon (8 sides) and triangle (3 sides)
        # Use a smooth transition function
        sides_float = 8 - 5 * (morph_factor ** 1.5)  # Non-linear transition
        sides = max(3, int(sides_float))
        
        # Create vertices
        angles = np.array([2*np.pi*k/sides for k in range(sides + 1)])  # +1 to close
        
        # Add some rotation based on the morph factor
        rotation = morph_factor * np.pi / 6
        angles += rotation
        
        x = cx + r * np.cos(angles)
        y = cy + r * np.sin(angles)
        
        # Line width varies with shape complexity
        lw = 1.0 + (8 - sides) * 0.3
        
        ax.plot(x, y, color="black", linewidth=lw, solid_capstyle="round", solid_joinstyle="round")

    save(fig, "abstract concentric geometric octagon morph triangle transition pattern black white texture")


if __name__ == "__main__":
    draw()