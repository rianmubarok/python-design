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
    Fluid Vortex Swirl.
    Concentric circles twisted by a vortex swirl in the center,
    distorting them into a spiral galaxy shape as they get sucked into the middle.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_circles = 40
    max_radius = 65.0
    
    n_pts = 600
    
    for i in range(1, n_circles + 1):
        r = max_radius * (i / n_circles)
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        # Base circle
        x_base = cx + r * np.cos(angles)
        y_base = cy + r * np.sin(angles)
        
        # Apply vortex rotation based on distance from center
        # Closer to center = more twist
        x_rot = np.zeros(n_pts)
        y_rot = np.zeros(n_pts)
        
        for j in range(n_pts):
            dx = x_base[j] - cx
            dy = y_base[j] - cy
            dist = np.sqrt(dx**2 + dy**2)
            
            # Twist angle decreases exponentially with distance
            twist = 8.0 * np.exp(-dist / 20.0)
            
            # Rotate point by twist angle
            cos_t = np.cos(twist)
            sin_t = np.sin(twist)
            
            x_rot[j] = cx + dx * cos_t - dy * sin_t
            y_rot[j] = cy + dx * sin_t + dy * cos_t
            
        ax.plot(x_rot, y_rot, color="black", linewidth=1.5, solid_capstyle="round")

    save(fig, "abstract concentric fluid vortex swirl distortion pattern black white texture")


if __name__ == "__main__":
    draw()
