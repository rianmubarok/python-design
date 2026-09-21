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
    3D Spherical Bulge (Op Art).
    Parallel lines passing over an invisible sphere.
    The lines bulge outward and their thickness increases as they 
    approach the apex of the sphere, creating a strong 3D optical illusion
    reminiscent of Victor Vasarely's op art.
    """
    fig, ax = setup_ax()

    n_lines = 100
    n_pts = 600

    cx, cy = 50.0, 50.0
    radius = 35.0

    from matplotlib.collections import LineCollection

    for i in range(n_lines):
        y0 = -5 + 110 * i / (n_lines - 1)
        x = np.linspace(-5, 105, n_pts)
        
        y_warped = np.full(n_pts, y0)
        lw = np.full(n_pts, 0.25)

        for j in range(n_pts):
            dx = x[j] - cx
            dy = y_warped[j] - cy
            r_sq = dx**2 + dy**2
            
            if r_sq < radius**2:
                # Point is inside the sphere boundary
                r = np.sqrt(r_sq)
                # Calculate z (height of the hemisphere)
                z = np.sqrt(radius**2 - r_sq)
                
                # Lens magnification effect (pushing points outward radially)
                # The closer to the center, the more it pushes outward in 2D projection
                mag = 1.0 + 0.4 * (z / radius)
                
                y_warped[j] = cy + dy * mag
                
                # Line thickness increases at the bulge (closer to camera)
                lw[j] = 0.25 + 0.85 * (z / radius)

        points = np.array([x, y_warped]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, linewidths=lw[:-1], colors="black", capstyle="round")
        ax.add_collection(lc)

    save(fig, "abstract parallel lines 3d spherical bulge op art pattern black white texture")


if __name__ == "__main__":
    draw()
