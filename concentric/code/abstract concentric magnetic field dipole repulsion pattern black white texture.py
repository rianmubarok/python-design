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
    Magnetic Field Dipole Repulsion.
    Concentric circles that are deformed and stretched by two repelling
    magnetic poles located inside the ring area.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_circles = 45
    max_radius = 65.0
    
    # Two repelling poles
    pole1 = np.array([40.0, 50.0])
    pole2 = np.array([60.0, 50.0])
    pole_strength = 200.0

    for i in range(1, n_circles + 1):
        r_base = max_radius * (i / n_circles)
        
        n_pts = 400
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        # Base circle points
        x = cx + r_base * np.cos(angles)
        y = cy + r_base * np.sin(angles)
        
        # Deform points based on inverse square repulsion from poles
        for j in range(n_pts):
            pt = np.array([x[j], y[j]])
            
            d1 = pt - pole1
            dist1 = np.linalg.norm(d1)
            dist1 = max(dist1, 3.0)
            push1 = d1 / dist1 * (pole_strength / (dist1 ** 2))
            
            d2 = pt - pole2
            dist2 = np.linalg.norm(d2)
            dist2 = max(dist2, 3.0)
            push2 = d2 / dist2 * (pole_strength / (dist2 ** 2))
            
            # Apply push
            x[j] += push1[0] + push2[0]
            y[j] += push1[1] + push2[1]
            
        # Draw deformed circle
        ax.plot(x, y, color="black", linewidth=1.5, solid_capstyle="round")

    save(fig, "abstract concentric magnetic field dipole repulsion pattern black white texture")


if __name__ == "__main__":
    draw()
