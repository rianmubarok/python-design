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
    """Flow based on cymatics - sound wave patterns that form nodal lines."""
    fig, ax = setup_ax()
    
    n_lines = 1800
    steps = 150
    step_size = 0.4
    
    # Sound frequency components
    frequencies = [0.1, 0.15, 0.08, 0.12]
    amplitudes = [1.0, 0.7, 0.5, 0.3]
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for step in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Calculate sound wave amplitude at current position
            wave_sum = 0
            gradient_x = 0
            gradient_y = 0
            
            for freq, amp in zip(frequencies, amplitudes):
                # Standing wave patterns
                wave_x = np.sin(x * freq * 2 * np.pi / 100)
                wave_y = np.sin(y * freq * 2 * np.pi / 100)
                
                # Circular modes (like drum head)
                r = np.sqrt((x - 50)**2 + (y - 50)**2)
                theta = np.arctan2(y - 50, x - 50)
                bessel_approx = np.sin(r * freq * 0.5) / (r * freq * 0.5 + 0.1)
                
                # Combined rectangular and circular modes
                wave_rect = wave_x * wave_y
                wave_circ = bessel_approx * np.sin(theta * 3 + step * 0.01)  # 3-fold symmetry
                
                wave = amp * (wave_rect + 0.5 * wave_circ)
                wave_sum += wave
                
                # Calculate gradient for flow direction
                dx_wave = amp * freq * 2 * np.pi / 100 * np.cos(x * freq * 2 * np.pi / 100) * wave_y
                dy_wave = amp * freq * 2 * np.pi / 100 * np.cos(y * freq * 2 * np.pi / 100) * wave_x
                
                gradient_x += dx_wave
                gradient_y += dy_wave
            
            # Particles flow along nodal lines (where amplitude is zero)
            # Flow perpendicular to gradient
            dx = -gradient_y * 0.5
            dy = gradient_x * 0.5
            
            # Add attraction to nodal lines
            nodal_attraction = abs(wave_sum) * 0.1
            dx -= gradient_x * nodal_attraction
            dy -= gradient_y * nodal_attraction
            
            # Oscillating motion due to sound
            oscillation_strength = 0.2
            dx += oscillation_strength * np.sin(step * 0.2)
            dy += oscillation_strength * np.cos(step * 0.15)
            
            # Boundary reflection (like sound in a box)
            if x < 5:
                dx = abs(dx)
            elif x > 95:
                dx = -abs(dx)
            if y < 5:
                dy = abs(dy)
            elif y > 95:
                dy = -abs(dy)
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            # Keep within bounds
            x = np.clip(x, 0, 100)
            y = np.clip(y, 0, 100)
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.25, linewidth=0.8)
            
    save(fig, "abstract flow cymatics sound wave nodal pattern black white texture")


if __name__ == "__main__":
    draw()