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
    Multi-Focal Lens Distortion.
    Concentric circles viewed through a grid of invisible magnifying lenses.
    The lines balloon outward locally and get thicker inside the lens zones.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_circles = 40
    max_radius = 65.0
    n_pts = 800
    
    # Define a 3x3 grid of lenses
    lenses = []
    for lx in [25.0, 50.0, 75.0]:
        for ly in [25.0, 50.0, 75.0]:
            if lx == 50.0 and ly == 50.0:
                continue # skip center
            lenses.append((lx, ly, 12.0, 2.5)) # x, y, radius, magnification

    from matplotlib.collections import LineCollection

    for i in range(1, n_circles + 1):
        r_base = max_radius * (i / n_circles)
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        x = cx + r_base * np.cos(angles)
        y = cy + r_base * np.sin(angles)
        
        lw = np.full(n_pts, 0.5)
        
        for j in range(n_pts):
            pt_x, pt_y = x[j], y[j]
            
            for lx, ly, lr, lmag in lenses:
                dx = pt_x - lx
                dy = pt_y - ly
                dist = np.sqrt(dx**2 + dy**2)
                
                if dist < lr:
                    # Inside the lens: magnify points away from the lens center
                    # and increase line thickness
                    t = dist / lr
                    # Dome-like magnification profile
                    mag_effect = (1 - t**2) * lmag
                    
                    x[j] += dx * mag_effect
                    y[j] += dy * mag_effect
                    lw[j] += mag_effect * 1.5

        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, linewidths=lw[:-1], colors="black", capstyle="round")
        ax.add_collection(lc)

    save(fig, "abstract concentric multi focal lens distortion pattern black white texture")


if __name__ == "__main__":
    draw()
