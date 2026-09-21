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
    Chladni Plate Cymatics (Standing waves).
    Simulates the resonant nodal lines of a square plate.
    The equation used: Z = sin(n*pi*x)*sin(m*pi*y) + sin(m*pi*x)*sin(n*pi*y)
    Lines are distorted and their thickness modulated by the amplitude of Z.
    """
    fig, ax = setup_ax()

    n_lines = 140
    n_pts = 600
    
    n, m = 3, 5  # Resonance modes

    for i in range(n_lines):
        y0 = -5 + 110 * i / (n_lines - 1)
        x = np.linspace(-5, 105, n_pts)
        
        # Normalize coordinates to 0..1 for the plate
        nx = (x + 5) / 110.0
        ny = (y0 + 5) / 110.0
        
        # Chladni function
        z = np.sin(n * np.pi * nx) * np.sin(m * np.pi * ny) - np.sin(m * np.pi * nx) * np.sin(n * np.pi * ny)
        
        # Warp the y position based on Z amplitude
        y_warped = y0 + 1.2 * z
        
        # Line width modulated by Z
        # Nodal lines (Z ~ 0) have different thickness than anti-nodes
        lw = 0.2 + 0.8 * np.exp(-10 * z**2)
        
        # Because line width varies, we plot segment by segment for smooth thickness transition,
        # but for performance we can plot as a few overlapping lines or use a scatter-like approach.
        # Alternatively, we just use a constant average line width for each line, but varying it
        # continuously looks much better. 
        # Matplotlib doesn't support varying linewidth in a single plot easily, so we use a PolyCollection
        # or just draw small segments.
        
        from matplotlib.collections import LineCollection
        points = np.array([x, y_warped]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, linewidths=lw[:-1], colors="black", capstyle="round")
        ax.add_collection(lc)

    save(fig, "abstract parallel lines cymatics chladni standing wave pattern black white texture")


if __name__ == "__main__":
    draw()
