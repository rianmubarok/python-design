import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from pathlib import Path
from datetime import datetime

# Configuration
SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

# Directory Management
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
EPS_DIR = OUTPUT_DIR / "eps"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)

def setup_ax():
    """Initialize axis coordinates (off, equal aspect, white background)."""
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax

def save(fig, name):
    """Save image in JPG and SVG formats."""
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
    print(f"Saved: {jpg_path} | {svg_path} | {eps_path}")

def draw():
    """
    Quantum Interference Hologram Pattern.
    Concentric circles modulated by quantum wave interference creating
    holographic-like patterns with phase shifts and probability clouds.
    """
    fig, ax = setup_ax()
    
    cx, cy = 50.0, 50.0
    n_circles = 80
    max_radius = 70.0
    n_pts = 800
    
    # Quantum interference parameters
    wavelengths = [3.5, 5.7, 8.2, 11.3]  # Multiple interference wavelengths
    phase_shifts = [0, np.pi/3, 2*np.pi/3, np.pi]  # Phase offsets
    amplitudes = [1.0, 0.7, 0.4, 0.2]  # Interference strengths
    
    for i in range(1, n_circles + 1):
        r_base = max_radius * (i / n_circles) ** 1.2
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        x_pts = []
        y_pts = []
        
        for j, angle in enumerate(angles):
            # Base position
            x_base = r_base * np.cos(angle)
            y_base = r_base * np.sin(angle)
            
            # Calculate quantum interference modulation
            interference = 0
            for k, (wavelength, phase, amplitude) in enumerate(zip(wavelengths, phase_shifts, amplitudes)):
                # Create standing wave pattern
                wave = np.sin(2 * np.pi * r_base / wavelength + phase)
                # Add angular quantum effects
                angular_wave = np.cos(angle * (k + 3) + phase)
                interference += amplitude * wave * angular_wave
            
            # Apply interference as radius modulation
            radius_mod = 1 + 0.3 * interference
            # Add probability cloud effect (quantum uncertainty)
            uncertainty = 0.1 * np.sin(angle * 7 + r_base * 0.5) * np.cos(r_base * 0.3)
            final_radius = r_base * radius_mod * (1 + uncertainty)
            
            x_final = cx + final_radius * np.cos(angle)
            y_final = cy + final_radius * np.sin(angle)
            
            x_pts.append(x_final)
            y_pts.append(y_final)
        
        # Create closed loop
        x_pts.append(x_pts[0])
        y_pts.append(y_pts[0])
        
        # Variable line width based on interference intensity
        base_interference = np.mean([np.sin(2 * np.pi * r_base / wl) for wl in wavelengths])
        lw = 0.8 + 0.5 * abs(base_interference)
        
        ax.plot(x_pts, y_pts, 'k-', linewidth=lw, alpha=0.9)
    
    save(fig, "abstract concentric quantum interference hologram pattern black white texture")

if __name__ == "__main__":
    draw()