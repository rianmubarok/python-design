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
    """Large-scale ocean gyre circulation with Coriolis effects."""
    fig, ax = setup_ax()
    
    n_lines = 2000
    steps = 250
    step_size = 0.25
    
    # Multiple gyre centers
    gyres = [
        (25, 75, 1),   # Northern gyre (clockwise in NH)
        (75, 75, 1),   # Another northern gyre
        (25, 25, -1),  # Southern gyre (counter-clockwise in SH)
        (75, 25, -1)   # Another southern gyre
    ]
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for step in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            dx, dy = 0, 0
            
            # Gyre circulation
            for gx, gy, rotation_sign in gyres:
                dist = np.sqrt((x - gx)**2 + (y - gy)**2) + 0.1
                
                if dist < 30:  # Within gyre influence
                    # Tangential velocity (circular flow)
                    angle = np.arctan2(y - gy, x - gx)
                    strength = (30 - dist) / 30 * 0.8
                    
                    vx = -rotation_sign * np.sin(angle) * strength
                    vy = rotation_sign * np.cos(angle) * strength
                    
                    # Modify for elliptical gyre shape
                    ellipse_factor = 1 + 0.3 * np.cos(angle * 2)
                    vx *= ellipse_factor
                    vy *= ellipse_factor
                    
                    dx += vx
                    dy += vy
            
            # Trade winds (east-west flow)
            if 25 < y < 75:  # Trade wind belt
                trade_strength = np.sin((y - 25) / 50 * np.pi) * 0.3
                dx += trade_strength
            
            # Westerlies (reverse direction)
            if y > 75 or y < 25:
                westerly_strength = 0.4
                dx -= westerly_strength
            
            # Coriolis effect
            coriolis_param = (y - 50) / 50 * 0.1  # f-parameter
            coriolis_x = -coriolis_param * dy
            coriolis_y = coriolis_param * dx
            
            dx += coriolis_x
            dy += coriolis_y
            
            # Continental boundary effects
            if x < 5 or x > 95:
                dx *= 0.1  # Slow near boundaries
            if y < 5 or y > 95:
                dy *= 0.1
            
            # Meandering and eddies
            eddy_x = 0.2 * np.sin(x * 0.1 + step * 0.02)
            eddy_y = 0.2 * np.cos(y * 0.1 + step * 0.02)
            
            dx += eddy_x
            dy += eddy_y
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.2, linewidth=0.8)
            
    save(fig, "abstract flow ocean current gyres circulation pattern black white texture")


if __name__ == "__main__":
    draw()