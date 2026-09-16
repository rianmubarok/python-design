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
    Tree Ring Noise Distortion.
    Concentric circles deformed by multiple layers of sine-based pseudo-noise,
    creating an organic, topographic, or tree-ring like texture.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    cx, cy = 50.0, 50.0
    n_circles = 45
    max_radius = 65.0
    n_pts = 600

    # Pseudo-noise setup
    octaves = []
    for i in range(4):
        freq_a = rng.uniform(2, 6) * (2 ** i)
        freq_b = rng.uniform(2, 6) * (2 ** i)
        amp = 4.0 / (2 ** i)
        phase = rng.uniform(0, 2*np.pi)
        octaves.append((freq_a, freq_b, amp, phase))

    for i in range(1, n_circles + 1):
        r_base = max_radius * (i / n_circles)
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        # Calculate noise based on angle and radius
        noise = np.zeros(n_pts)
        for fa, fb, amp, ph in octaves:
            # Domain warping using angle
            noise += np.sin(angles * fa + ph) * np.cos(angles * fb) * amp
            
        # The noise displaces the radius
        # Fade noise out towards the center so it doesn't cross itself too much
        fade = min(1.0, r_base / 15.0)
        r = r_base + noise * fade * 1.5
        
        # To make it a closed loop smoothly, ensure the noise matches at 0 and 2pi
        # Actually since it's sin(angles * integer), it should inherently wrap if frequencies are integers.
        # Wait, fa and fb are floats. Let's force them to be integers to ensure perfect looping!
        
    # Re-setup octaves with integers
    rng = np.random.default_rng(42)
    octaves = []
    for i in range(4):
        fa = int(rng.uniform(2, 6) * (2 ** i))
        fb = int(rng.uniform(2, 6) * (2 ** i))
        amp = 4.0 / (2 ** i)
        phase = rng.uniform(0, 2*np.pi)
        octaves.append((fa, fb, amp, phase))
        
    for i in range(1, n_circles + 1):
        r_base = max_radius * (i / n_circles)
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        noise = np.zeros(n_pts)
        for fa, fb, amp, ph in octaves:
            noise += np.sin(angles * fa + ph) * np.cos(angles * fb) * amp
            
        fade = min(1.0, (r_base / 15.0)**1.5)
        r = r_base + noise * fade * 1.5
        
        x = cx + r * np.cos(angles)
        y = cy + r * np.sin(angles)
        
        ax.plot(x, y, color="black", linewidth=1.2, solid_capstyle="round", solid_joinstyle="round")

    save(fig, "abstract concentric circles tree ring noise distortion pattern black white texture")


if __name__ == "__main__":
    draw()
