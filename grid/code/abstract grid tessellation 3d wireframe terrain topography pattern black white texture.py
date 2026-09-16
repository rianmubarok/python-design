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
    3D Wireframe Terrain Topography.
    A rectangular grid distorted by 3D pseudo-noise and projected in perspective
    to look like a retro wireframe mountain landscape.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    n_lines = 40
    # Grid in 3D space
    x = np.linspace(-30, 130, n_lines)
    z = np.linspace(10, 150, n_lines)
    X, Z = np.meshgrid(x, z)
    
    # Generate Perlin-like noise for Y (height)
    Y = np.zeros_like(X)
    for f in [0.03, 0.08, 0.15]:
        phase_x = rng.uniform(0, 2*np.pi)
        phase_z = rng.uniform(0, 2*np.pi)
        amp = 1.0 / f
        Y += np.sin(X * f + phase_x) * np.cos(Z * f + phase_z) * amp * 0.4
        
    # Project 3D (X, Y, Z) to 2D (screen_x, screen_y) using simple perspective
    cam_z = -50
    fov = 120.0
    
    screen_x = np.zeros_like(X)
    screen_y = np.zeros_like(X)
    
    for i in range(n_lines):
        for j in range(n_lines):
            # Depth
            depth = Z[i, j] - cam_z
            # Perspective divide
            screen_x[i, j] = 50.0 + (X[i, j] - 50.0) * fov / depth
            screen_y[i, j] = 10.0 + Y[i, j] * (fov / depth) + (depth * 0.4) # tilt down

    # Draw horizontal grid lines
    for i in range(n_lines):
        ax.plot(screen_x[i, :], screen_y[i, :], color="black", linewidth=1.0)
        
    # Draw vertical grid lines
    for j in range(n_lines):
        ax.plot(screen_x[:, j], screen_y[:, j], color="black", linewidth=1.0)

    save(fig, "abstract grid tessellation 3d wireframe terrain topography pattern black white texture")


if __name__ == "__main__":
    draw()
