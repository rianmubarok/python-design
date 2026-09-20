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
    """Yin-Yang inspired flow with dual circulation and balance."""
    fig, ax = setup_ax()
    
    n_lines = 2200
    steps = 200
    step_size = 0.25
    
    center_x, center_y = 50, 50
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for step in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Distance and angle from center
            r = np.sqrt((x - center_x)**2 + (y - center_y)**2) + 0.1
            theta = np.arctan2(y - center_y, x - center_x)
            
            # Yin-Yang division (S-curve)
            s_curve = np.sin(theta + np.sin(theta * 2) * 0.5)
            
            # Determine which side (yin or yang)
            if s_curve > 0:
                # Yang side - clockwise circulation
                circulation_sign = 1
            else:
                # Yin side - counter-clockwise circulation
                circulation_sign = -1
            
            # Base circular flow
            base_strength = 0.8 * (40 - min(r, 39)) / 40
            if base_strength > 0:
                vx = -circulation_sign * (y - center_y) * base_strength * 0.02
                vy = circulation_sign * (x - center_x) * base_strength * 0.02
            else:
                vx, vy = 0, 0
            
            # S-curve interface dynamics
            interface_distance = abs(s_curve) 
            if interface_distance < 0.2:  # Near the S-curve interface
                # Flow along the interface
                interface_tangent_x = np.cos(theta + np.pi/2 + np.cos(theta * 2))
                interface_tangent_y = np.sin(theta + np.pi/2 + np.cos(theta * 2))
                
                interface_strength = (0.2 - interface_distance) / 0.2 * 0.5
                vx += interface_tangent_x * interface_strength
                vy += interface_tangent_y * interface_strength
            
            # Small circulation centers (dots in yin-yang)
            dot1_x, dot1_y = center_x, center_y + 15  # Yang dot
            dot2_x, dot2_y = center_x, center_y - 15  # Yin dot
            
            # Yang dot influence (small yin circulation)
            r1 = np.sqrt((x - dot1_x)**2 + (y - dot1_y)**2) + 0.1
            if r1 < 8:
                dot_strength = (8 - r1) / 8 * 0.3
                vx += (y - dot1_y) * dot_strength * 0.05  # Counter-clockwise
                vy += -(x - dot1_x) * dot_strength * 0.05
            
            # Yin dot influence (small yang circulation) 
            r2 = np.sqrt((x - dot2_x)**2 + (y - dot2_y)**2) + 0.1
            if r2 < 8:
                dot_strength = (8 - r2) / 8 * 0.3
                vx += -(y - dot2_y) * dot_strength * 0.05  # Clockwise
                vy += (x - dot2_x) * dot_strength * 0.05
            
            # Dynamic balance (breathing motion)
            balance_phase = step * 0.01
            balance_amplitude = 0.1
            vx += balance_amplitude * np.sin(balance_phase + theta)
            vy += balance_amplitude * np.cos(balance_phase + theta)
            
            # Harmonic resonance
            harmonic_x = 0.15 * np.sin(theta * 3 + step * 0.02)
            harmonic_y = 0.15 * np.cos(theta * 3 + step * 0.02)
            
            dx = vx + harmonic_x
            dy = vy + harmonic_y
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.25, linewidth=0.7)
            
    save(fig, "abstract flow yin yang duality tao circulation pattern black white texture")


if __name__ == "__main__":
    draw()