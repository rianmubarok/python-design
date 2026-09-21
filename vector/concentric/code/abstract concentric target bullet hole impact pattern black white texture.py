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
    Target Bullet Hole Impact.
    A concentric target pattern distorted by several simulated 
    impact craters (bullet holes) that rip and tear the rings inward.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    cx, cy = 50.0, 50.0
    n_circles = 35
    max_radius = 65.0
    n_pts = 800
    
    # Define impacts: (x, y, radius, strength)
    impacts = [
        (40.0, 60.0, 8.0, 15.0),
        (65.0, 35.0, 6.0, 10.0),
        (30.0, 30.0, 5.0, 8.0),
        (75.0, 70.0, 7.0, 12.0)
    ]

    for i in range(1, n_circles + 1):
        r_base = max_radius * (i / n_circles)
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        x = cx + r_base * np.cos(angles)
        y = cy + r_base * np.sin(angles)
        
        x_distorted = np.copy(x)
        y_distorted = np.copy(y)
        
        # Apply impact distortion
        for ix, iy, ir, i_strength in impacts:
            for j in range(n_pts):
                dx = x[j] - ix
                dy = y[j] - iy
                dist = np.sqrt(dx**2 + dy**2)
                
                if dist < ir * 3.0:
                    # Rings get sucked into the impact hole
                    pull = i_strength * np.exp(-(dist / ir)**2)
                    
                    if dist > 0.1:
                        # Adding jagged tearing near the center of the impact
                        tear = 0.0
                        if dist < ir:
                            tear = rng.normal(0, 0.5) * (ir - dist)
                            
                        x_distorted[j] -= (dx / dist) * pull + tear
                        y_distorted[j] -= (dy / dist) * pull + tear
                        
                        # Sometimes lines break entirely in the crater
                        if dist < ir * 0.4 and rng.random() > 0.5:
                            x_distorted[j] = np.nan
                            y_distorted[j] = np.nan

        ax.plot(x_distorted, y_distorted, color="black", linewidth=1.5, solid_capstyle="round")

    # Add scattered fragments around impacts
    for ix, iy, ir, i_strength in impacts:
        for _ in range(20):
            fx = ix + rng.normal(0, ir * 1.5)
            fy = iy + rng.normal(0, ir * 1.5)
            ax.plot([fx, fx + rng.normal(0, 1.0)], [fy, fy + rng.normal(0, 1.0)], 
                    color="black", linewidth=1.0)

    save(fig, "abstract concentric target bullet hole impact pattern black white texture")


if __name__ == "__main__":
    draw()
