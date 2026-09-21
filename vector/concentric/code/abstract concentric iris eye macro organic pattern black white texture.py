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
EPS_DIR = OUTPUT_DIR / "eps"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


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
    eps_path = EPS_DIR / f"{name} {DATE}.eps"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    # Save EPS with larger figure size for 4MP+ bounding box
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format="eps", pad_inches=0, facecolor="white", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path} | {eps_path}")


def draw():
    """
    Organic Iris Eye Macro.
    Concentric rings that look like the intricate fibrous structure of a 
    human iris. Rings have high-frequency radial noise and jagged variations
    in thickness and placement.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    cx, cy = 50.0, 50.0
    n_circles = 50
    max_radius = 65.0
    n_pts = 800

    # Base noise pattern for the iris crypts (craters)
    crypt_angles = rng.uniform(0, 2*np.pi, 15)
    crypt_radii = rng.uniform(15, 45, 15)
    crypt_sizes = rng.uniform(3, 10, 15)

    from matplotlib.collections import LineCollection

    for i in range(1, n_circles + 1):
        r_base = max_radius * (i / n_circles)
        
        # Pupil (black void in center)
        if r_base < 10.0:
            circle = plt.Circle((cx, cy), r_base, color="black", fill=True)
            ax.add_patch(circle)
            continue
            
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        # High frequency jitter simulating muscle fibers
        jitter = np.sin(angles * int(rng.uniform(40, 120))) * rng.uniform(0.1, 0.8)
        # Medium frequency structure
        structure = np.sin(angles * int(rng.uniform(10, 30)) + rng.uniform(0, 2*np.pi)) * 1.5
        
        r = r_base + jitter + structure
        
        # Add crypts (indentations)
        for ca, cr, cs in zip(crypt_angles, crypt_radii, crypt_sizes):
            # Distance from crypt center
            angular_dist = np.abs(angles - ca)
            angular_dist = np.minimum(angular_dist, 2*np.pi - angular_dist) # wrap around
            radial_dist = np.abs(r_base - cr)
            
            dist = np.sqrt((angular_dist * r_base)**2 + radial_dist**2)
            
            if np.any(dist < cs):
                r -= np.exp(-(dist/cs)**2) * 3.0
        
        x = cx + r * np.cos(angles)
        y = cy + r * np.sin(angles)
        
        lw = 0.3 + 1.2 * rng.random(n_pts)
        # Smoothing line width
        lw = np.convolve(lw, np.ones(10)/10.0, mode='same')
        
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, linewidths=lw[:-1], colors="black", capstyle="round")
        ax.add_collection(lc)

    save(fig, "abstract concentric iris eye macro organic pattern black white texture")


if __name__ == "__main__":
    draw()
