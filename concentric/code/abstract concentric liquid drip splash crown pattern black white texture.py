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
    Liquid Drip Splash Crown.
    Concentric rings that get pushed upwards violently in a radial "crown" 
    shape, imitating a slow-motion milk drop splash. Outer rings break 
    into suspended droplets.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    cx, cy = 50.0, 50.0
    n_circles = 35
    max_radius = 55.0
    n_pts = 600
    
    n_spikes = 14
    spike_angles = np.linspace(0, 2*np.pi, n_spikes, endpoint=False) + rng.uniform(0, 0.5)

    for i in range(1, n_circles + 1):
        t = i / n_circles
        r_base = max_radius * t
        
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        # Calculate spike deformation
        spike_deformation = np.zeros(n_pts)
        for sa in spike_angles:
            # Gaussian peaks around each spike angle
            angular_dist = np.abs(angles - sa)
            angular_dist = np.minimum(angular_dist, 2*np.pi - angular_dist)
            # Spikes grow taller and sharper on the outer rings
            height = 25.0 * (t ** 2)
            width = 0.2 * (1.1 - t)
            spike_deformation += height * np.exp(-(angular_dist / width)**2)
            
        r = r_base + spike_deformation
        
        x = cx + r * np.cos(angles)
        y = cy + r * np.sin(angles)
        
        # On outer rings, lines break and form droplets at the tips of the spikes
        if t > 0.7:
            # Mask out the sharpest parts of the spikes to create gaps
            derivative = np.abs(np.gradient(r))
            gap_mask = derivative > (5.0 * t)
            
            x_plot = np.where(gap_mask, np.nan, x)
            y_plot = np.where(gap_mask, np.nan, y)
            
            ax.plot(x_plot, y_plot, color="black", linewidth=1.5, solid_capstyle="round")
            
            # Draw droplet dots at the very tips
            if t > 0.85:
                for sa in spike_angles:
                    tip_r = r_base + 25.0 * (t ** 2) + rng.uniform(1.0, 5.0)
                    tip_x = cx + tip_r * np.cos(sa)
                    tip_y = cy + tip_r * np.sin(sa)
                    circle = plt.Circle((tip_x, tip_y), rng.uniform(0.5, 1.2), color="black", fill=True)
                    ax.add_patch(circle)
        else:
            ax.plot(x, y, color="black", linewidth=1.5, solid_capstyle="round")

    save(fig, "abstract concentric liquid drip splash crown pattern black white texture")


if __name__ == "__main__":
    draw()
