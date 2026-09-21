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
    """Flow based on quantum wave function interference patterns."""
    fig, ax = setup_ax()
    
    n_lines = 1800
    steps = 200
    step_size = 0.3
    
    # Quantum wave sources (like double-slit experiment)
    wave_sources = [(20, 50), (40, 50), (60, 50), (80, 50)]
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for step in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Calculate wave interference pattern
            wave_amplitude = 0
            phase_gradient_x = 0
            phase_gradient_y = 0
            
            for i, (sx, sy) in enumerate(wave_sources):
                # Distance to source
                r = np.sqrt((x - sx)**2 + (y - sy)**2) + 0.1
                
                # Wave number and frequency
                k = 0.3 + i * 0.1  # Different wavelengths
                omega = step * 0.02
                
                # Phase
                phase = k * r - omega
                
                # Wave amplitude (decreases with distance)
                amplitude = 1.0 / np.sqrt(r)
                
                # Complex wave (using real part for flow)
                wave = amplitude * np.exp(1j * phase)
                wave_amplitude += wave
                
                # Gradient of phase for flow direction
                dphi_dx = k * (x - sx) / r
                dphi_dy = k * (y - sy) / r
                
                phase_gradient_x += amplitude * dphi_dx
                phase_gradient_y += amplitude * dphi_dy
            
            # Probability current (quantum flow)
            probability = abs(wave_amplitude)**2
            
            # Flow direction based on phase gradient and probability
            dx = phase_gradient_x * probability * 0.1
            dy = phase_gradient_y * probability * 0.1
            
            # Add quantum tunneling effect (random jumps)
            if np.random.random() < 0.05:
                dx += np.random.normal(0, 2)
                dy += np.random.normal(0, 2)
            
            # Normalize but preserve quantum uncertainty
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.2, linewidth=0.7)
            
    save(fig, "abstract flow quantum probability wave interference pattern black white texture")


if __name__ == "__main__":
    draw()