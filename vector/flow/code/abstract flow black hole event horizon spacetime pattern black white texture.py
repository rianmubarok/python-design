import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
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
    """Black hole spacetime curvature with event horizon and Hawking radiation."""
    fig, ax = setup_ax()
    
    n_lines = 2500
    steps = 200
    step_size = 0.25
    
    # Black hole parameters
    bh_x, bh_y = 50, 50
    schwarzschild_radius = 8  # Event horizon
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for step in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Distance from black hole
            r = np.sqrt((x - bh_x)**2 + (y - bh_y)**2) + 0.001
            
            if r < schwarzschild_radius * 0.9:
                # Inside event horizon - all paths lead inward
                dx = -(x - bh_x) * 2.0 / r
                dy = -(y - bh_y) * 2.0 / r
                
                # Time dilation effects (slower motion)
                dx *= 0.1
                dy *= 0.1
                
            elif r < schwarzschild_radius * 3:
                # Near event horizon - extreme spacetime curvature
                
                # Gravitational attraction (1/r^2)
                gravity_strength = 100.0 / (r**2)
                gx = -(x - bh_x) / r * gravity_strength
                gy = -(y - bh_y) / r * gravity_strength
                
                # Frame dragging (rotation of spacetime)
                angle = np.arctan2(y - bh_y, x - bh_x)
                frame_drag_strength = 20.0 / (r**1.5)
                fdx = -frame_drag_strength * np.sin(angle)
                fdy = frame_drag_strength * np.cos(angle)
                
                # Tidal effects (differential gravity)
                tidal_strength = 50.0 / (r**3)
                # Stretch radially, compress tangentially
                radial_unit_x = (x - bh_x) / r
                radial_unit_y = (y - bh_y) / r
                
                tidal_x = radial_unit_x * tidal_strength * 0.1
                tidal_y = radial_unit_y * tidal_strength * 0.1
                
                dx = gx + fdx + tidal_x
                dy = gy + fdy + tidal_y
                
                # Redshift effects (frequency scaling)
                redshift_factor = np.sqrt(1 - schwarzschild_radius / r)
                dx *= redshift_factor
                dy *= redshift_factor
                
            else:
                # Far field - weak gravitational lensing
                
                # Weak gravity
                gravity_strength = 15.0 / (r**2)
                gx = -(x - bh_x) / r * gravity_strength
                gy = -(y - bh_y) / r * gravity_strength
                
                # Geodesic precession
                angle = np.arctan2(y - bh_y, x - bh_x)
                precession = 0.5 / r
                px = -precession * np.sin(angle)
                py = precession * np.cos(angle)
                
                dx = gx + px
                dy = gy + py
                
                # Hawking radiation (random outward flow)
                if r > schwarzschild_radius * 2 and r < schwarzschild_radius * 4:
                    hawking_strength = np.exp(-(r - schwarzschild_radius * 2)) * 0.3
                    hawking_x = np.random.normal(0, hawking_strength)
                    hawking_y = np.random.normal(0, hawking_strength)
                    
                    # Bias outward
                    hawking_x += (x - bh_x) / r * hawking_strength * 0.5
                    hawking_y += (y - bh_y) / r * hawking_strength * 0.5
                    
                    dx += hawking_x
                    dy += hawking_y
            
            # Accretion disk effects (if in disk plane)
            disk_thickness = 3
            if abs(y - bh_y) < disk_thickness and r > schwarzschild_radius:
                # Keplerian orbital velocity
                orbital_speed = np.sqrt(30.0 / r) if r > schwarzschild_radius else 0
                
                # Tangential velocity
                angle = np.arctan2(y - bh_y, x - bh_x)
                orbit_x = -orbital_speed * np.sin(angle) * 0.3
                orbit_y = orbital_speed * np.cos(angle) * 0.3
                
                # Viscous inward drift
                viscous_x = -(x - bh_x) / r * 0.1
                viscous_y = -(y - bh_y) / r * 0.1
                
                dx += orbit_x + viscous_x
                dy += orbit_y + viscous_y
            
            # Photon sphere (unstable circular orbits)
            photon_sphere = schwarzschild_radius * 1.5
            if abs(r - photon_sphere) < 1:
                # Circular motion at photon sphere
                angle = np.arctan2(y - bh_y, x - bh_x)
                circular_strength = (1 - abs(r - photon_sphere)) * 0.8
                dx += -circular_strength * np.sin(angle)
                dy += circular_strength * np.cos(angle)
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.2, linewidth=0.7)
            
    save(fig, "abstract flow black hole event horizon spacetime pattern black white texture")


if __name__ == "__main__":
    draw()