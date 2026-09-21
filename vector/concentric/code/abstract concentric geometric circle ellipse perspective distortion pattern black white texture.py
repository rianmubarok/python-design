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
    Geometric Circle Ellipse Perspective Distortion.
    Concentric circles that gradually transform into ellipses with perspective distortion,
    simulating a 3D tunnel viewed at an angle.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_shapes = 45
    max_radius = 65.0
    
    for i in range(1, n_shapes + 1):
        r = max_radius * (i / n_shapes)
        
        # Perspective distortion factor: increases toward edges
        perspective_factor = (i / n_shapes) ** 1.8
        
        # Ellipse parameters
        # Y-axis gets compressed (perspective effect)
        a = r  # X semi-axis remains circular
        b = r * (1.0 - 0.6 * perspective_factor)  # Y semi-axis compressed
        
        # Vertical offset increases with perspective (vanishing point effect)
        offset_y = perspective_factor * 8.0
        
        # Rotation increases with distance (perspective twist)
        rotation = perspective_factor * np.pi / 8
        
        # Generate ellipse points
        angles = np.linspace(0, 2*np.pi, 300)
        x_ellipse = a * np.cos(angles)
        y_ellipse = b * np.sin(angles)
        
        # Apply rotation
        cos_rot = np.cos(rotation)
        sin_rot = np.sin(rotation)
        x_rotated = x_ellipse * cos_rot - y_ellipse * sin_rot
        y_rotated = x_ellipse * sin_rot + y_ellipse * cos_rot
        
        # Final position with offset
        x_final = cx + x_rotated
        y_final = cy + y_rotated - offset_y
        
        # Line width decreases with perspective (depth effect)
        lw = 2.2 - 1.4 * perspective_factor
        lw = max(0.5, lw)
        
        ax.plot(x_final, y_final, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract concentric geometric circle ellipse perspective distortion pattern black white texture")


if __name__ == "__main__":
    draw()