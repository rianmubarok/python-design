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
    """Hyperbolic saddle point flow with multiple saddle points."""
    fig, ax = setup_ax()
    
    n_lines = 2200
    steps = 120
    step_size = 0.4
    
    # Multiple saddle points
    saddle_points = [(25, 25), (75, 25), (25, 75), (75, 75), (50, 50)]
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for _ in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            dx, dy = 0, 0
            
            # Sum contributions from all saddle points
            for sx, sy in saddle_points:
                # Translate to saddle-centered coordinates
                u = (x - sx) / 10  # Scale factor for stability
                v = (y - sy) / 10
                
                # Hyperbolic saddle: du/dt = u, dv/dt = -v
                saddle_strength = 1.0 / (np.sqrt(u**2 + v**2) + 0.5)
                
                # Saddle flow field
                du_dt = u * saddle_strength
                dv_dt = -v * saddle_strength
                
                # Transform back and accumulate
                dx += du_dt * 0.8
                dy += dv_dt * 0.8
            
            # Add rotational component to prevent pure divergence
            rotation_strength = 0.2
            center_x, center_y = 50, 50
            rx = x - center_x
            ry = y - center_y
            
            dx += -ry * rotation_strength * 0.01
            dy += rx * rotation_strength * 0.01
            
            # Non-linear perturbations
            dx += 0.3 * np.sin(x * 0.15 + y * 0.1)
            dy += 0.3 * np.cos(x * 0.1 + y * 0.15)
            
            # Heteroclinic connections (flow between saddles)
            for i, (sx1, sy1) in enumerate(saddle_points):
                for sx2, sy2 in saddle_points[i+1:]:
                    # Create connecting flow
                    midx, midy = (sx1 + sx2) / 2, (sy1 + sy2) / 2
                    dist_to_connection = np.sqrt((x - midx)**2 + (y - midy)**2)
                    
                    if dist_to_connection < 15:
                        connection_strength = np.exp(-dist_to_connection / 5)
                        dx += (sx2 - sx1) * connection_strength * 0.02
                        dy += (sy2 - sy1) * connection_strength * 0.02
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.25, linewidth=0.8)
            
    save(fig, "abstract flow vector field hyperbolic saddle pattern black white texture")


if __name__ == "__main__":
    draw()