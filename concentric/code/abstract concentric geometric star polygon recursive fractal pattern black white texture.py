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


def draw_star(cx, cy, r_outer, r_inner, n_points, rotation=0):
    """Draw a star polygon with specified parameters."""
    angles_outer = np.array([rotation + 2*np.pi*k/n_points for k in range(n_points)])
    angles_inner = angles_outer + np.pi/n_points
    
    x_coords = []
    y_coords = []
    
    for i in range(n_points):
        # Outer point
        x_coords.append(cx + r_outer * np.cos(angles_outer[i]))
        y_coords.append(cy + r_outer * np.sin(angles_outer[i]))
        # Inner point
        x_coords.append(cx + r_inner * np.cos(angles_inner[i]))
        y_coords.append(cy + r_inner * np.sin(angles_inner[i]))
    
    # Close the star
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0])
    
    return np.array(x_coords), np.array(y_coords)


def draw():
    """
    Geometric Star Polygon Recursive Fractal.
    Concentric star polygons with varying point counts and recursive subdivisions,
    creating a complex fractal-like pattern.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_layers = 28
    max_radius = 65.0
    
    for i in range(1, n_layers + 1):
        r_outer = max_radius * (i / n_layers)
        
        # Vary star complexity: cycle through different point counts
        point_cycle = [5, 6, 7, 8, 12]  # Various star types
        n_points = point_cycle[(i - 1) % len(point_cycle)]
        
        # Inner radius ratio varies with layer
        inner_ratio = 0.3 + 0.4 * np.sin(i * np.pi / 8)  # Oscillating inner ratio
        r_inner = r_outer * inner_ratio
        
        # Progressive rotation
        rotation = i * np.pi / 12
        
        x_star, y_star = draw_star(cx, cy, r_outer, r_inner, n_points, rotation)
        
        # Line properties
        if i % 3 == 0:
            # Thick stars every 3rd layer
            ax.plot(x_star, y_star, color="black", linewidth=2.2, solid_capstyle="round", solid_joinstyle="round")
        elif i % 7 == 0:
            # Dashed stars every 7th layer
            ax.plot(x_star, y_star, color="black", linewidth=1.5, linestyle=(0, (5, 3)), solid_capstyle="round")
        else:
            # Regular stars
            ax.plot(x_star, y_star, color="black", linewidth=1.0, solid_capstyle="round", solid_joinstyle="round")

    save(fig, "abstract concentric geometric star polygon recursive fractal pattern black white texture")


if __name__ == "__main__":
    draw()