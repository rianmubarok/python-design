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
    Audio Waveform Spectrum Visualizer.
    Concentric circles deformed by sharp radial spikes imitating an 
    audio frequency spectrum analyzer. Spikes pulse outward.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    cx, cy = 50.0, 50.0
    n_circles = 30
    max_radius = 55.0
    n_pts = 600
    
    # Generate random spectrum peaks
    n_peaks = 32
    peak_angles = np.linspace(0, 2*np.pi, n_peaks, endpoint=False)
    # Add random jitter to peak positions
    peak_angles += rng.uniform(-0.05, 0.05, n_peaks)
    
    # Peak amplitudes (some very tall, some short)
    peak_amps = rng.exponential(scale=6.0, size=n_peaks)
    
    # Only deform the outer rings strongly
    for i in range(1, n_circles + 1):
        t = i / n_circles
        r_base = max_radius * t
        
        angles = np.linspace(0, 2 * np.pi, n_pts)
        r = np.full(n_pts, r_base)
        
        # Deformation strength scales heavily with distance from center
        strength = t ** 3
        
        for pa, pa_amp in zip(peak_angles, peak_amps):
            # Calculate distance to peak angle
            adist = np.abs(angles - pa)
            adist = np.minimum(adist, 2*np.pi - adist)
            
            # Sharp spikes using inverse absolute distance (triangle-like wave)
            spike = np.maximum(0, 1.0 - (adist / 0.08))
            
            r += spike * pa_amp * strength
            
        x = cx + r * np.cos(angles)
        y = cy + r * np.sin(angles)
        
        ax.plot(x, y, color="black", linewidth=1.5, solid_capstyle="round", solid_joinstyle="miter")

    save(fig, "abstract concentric audio waveform spectrum visualizer pattern black white texture")


if __name__ == "__main__":
    draw()
