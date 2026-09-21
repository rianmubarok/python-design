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
    Gravity Slingshot Teardrop Orbit.
    Concentric rings pulled intensely into a teardrop shape by a massive
    gravitational body passing by on the right side.
    """
    fig, ax = setup_ax()

    cx, cy = 40.0, 50.0  # Shift center to the left
    n_circles = 45
    max_radius = 50.0
    n_pts = 600
    
    # Gravitational mass location
    gx, gy = 95.0, 50.0
    mass_strength = 2500.0

    for i in range(1, n_circles + 1):
        r_base = max_radius * (i / n_circles)
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        x = cx + r_base * np.cos(angles)
        y = cy + r_base * np.sin(angles)
        
        # Apply inverse-square gravity pull towards gx, gy
        for j in range(n_pts):
            dx = gx - x[j]
            dy = gy - y[j]
            dist = np.sqrt(dx**2 + dy**2)
            
            # Avoid singularity
            dist = max(dist, 5.0)
            
            pull = mass_strength / (dist ** 2)
            
            x[j] += (dx / dist) * pull
            y[j] += (dy / dist) * pull
            
        ax.plot(x, y, color="black", linewidth=1.2, solid_capstyle="round")

    save(fig, "abstract concentric gravity slingshot teardrop orbit pattern black white texture")


if __name__ == "__main__":
    draw()
