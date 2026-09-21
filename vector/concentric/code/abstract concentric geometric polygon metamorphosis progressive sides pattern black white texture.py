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
    Geometric Polygon Metamorphosis Progressive Sides.
    Concentric polygons that progressively increase in side count from center to edge,
    creating a smooth metamorphosis from triangle to high-order polygons (approaching circle).
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_shapes = 50
    max_radius = 65.0
    
    # Side count progression: from 3 (triangle) to 24 (near-circle)
    min_sides = 3
    max_sides = 24
    
    for i in range(1, n_shapes + 1):
        r = max_radius * (i / n_shapes)
        
        # Progressive side count with smooth exponential curve
        progress = (i - 1) / (n_shapes - 1)
        sides_float = min_sides + (max_sides - min_sides) * (progress ** 0.7)
        sides = int(round(sides_float))
        sides = max(min_sides, min(sides, max_sides))
        
        # Rotation to align shapes nicely
        base_rotation = np.pi / sides  # Align flat edge with horizontal
        progressive_rotation = progress * np.pi / 8  # Additional subtle rotation
        rotation = base_rotation + progressive_rotation
        
        # Generate polygon vertices
        angles = np.array([rotation + 2*np.pi*k/sides for k in range(sides + 1)])  # +1 to close
        
        x = cx + r * np.cos(angles)
        y = cy + r * np.sin(angles)
        
        # Line properties based on polygon complexity
        if sides <= 4:  # Low complexity (triangle, square)
            lw = 2.0
            style = "solid"
        elif sides <= 8:  # Medium complexity
            lw = 1.6
            style = "solid"
        elif sides <= 12:  # High complexity
            lw = 1.3
            style = (0, (3, 2))  # Dashed
        else:  # Very high complexity (near-circle)
            lw = 1.0
            style = (0, (1, 1))  # Dotted
        
        if isinstance(style, str):
            ax.plot(x, y, color="black", linewidth=lw, linestyle=style, 
                   solid_capstyle="round", solid_joinstyle="round")
        else:
            ax.plot(x, y, color="black", linewidth=lw, linestyle=style, 
                   solid_capstyle="round")

    save(fig, "abstract concentric geometric polygon metamorphosis progressive sides pattern black white texture")


if __name__ == "__main__":
    draw()