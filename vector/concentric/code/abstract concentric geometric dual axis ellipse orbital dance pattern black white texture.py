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
    Geometric Dual Axis Ellipse Orbital Dance.
    Concentric ellipses with two different rotation axes creating an orbital dance effect.
    Each ellipse has unique eccentricity and rotates around alternating axes.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_shapes = 38
    max_radius = 65.0
    
    for i in range(1, n_shapes + 1):
        r = max_radius * (i / n_shapes)
        
        # Alternate between two rotation centers (dual axis effect)
        if i % 2 == 0:
            # Even layers: rotate around offset axis 1
            center_x = cx + 8 * np.cos(i * np.pi / 10)
            center_y = cy + 4 * np.sin(i * np.pi / 15)
            main_rotation = i * np.pi / 12
        else:
            # Odd layers: rotate around offset axis 2
            center_x = cx - 6 * np.cos(i * np.pi / 8)
            center_y = cy - 3 * np.sin(i * np.pi / 12)
            main_rotation = -i * np.pi / 16
        
        # Ellipse parameters with varying eccentricity
        eccentricity = 0.3 + 0.5 * np.sin(i * np.pi / 6)  # Oscillating eccentricity
        
        # Semi-axes
        a = r  # Major axis
        b = r * (1 - eccentricity)  # Minor axis (creates ellipse)
        
        # Orbital rotation: ellipse orientation changes
        orbital_rotation = i * np.pi / 20
        total_rotation = main_rotation + orbital_rotation
        
        # Generate ellipse points
        angles = np.linspace(0, 2*np.pi, 250)
        x_ellipse = a * np.cos(angles)
        y_ellipse = b * np.sin(angles)
        
        # Apply rotation
        cos_rot = np.cos(total_rotation)
        sin_rot = np.sin(total_rotation)
        x_rotated = x_ellipse * cos_rot - y_ellipse * sin_rot
        y_rotated = x_ellipse * sin_rot + y_ellipse * cos_rot
        
        # Final positioning
        x_final = center_x + x_rotated
        y_final = center_y + y_rotated
        
        # Line properties
        if i % 4 == 0:
            # Every 4th ellipse: thick and dashed
            ax.plot(x_final, y_final, color="black", linewidth=2.2, 
                   linestyle=(0, (4, 3)), solid_capstyle="round")
        elif eccentricity > 0.6:
            # High eccentricity: thin lines
            ax.plot(x_final, y_final, color="black", linewidth=0.8, solid_capstyle="round")
        else:
            # Normal ellipses
            ax.plot(x_final, y_final, color="black", linewidth=1.4, solid_capstyle="round")

    save(fig, "abstract concentric geometric dual axis ellipse orbital dance pattern black white texture")


if __name__ == "__main__":
    draw()