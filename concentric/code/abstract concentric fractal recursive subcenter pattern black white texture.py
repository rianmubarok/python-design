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
    Fractal Recursive Sub-centers.
    A main set of concentric circles, but smaller sets of concentric circles
    spawn on the outer rings, recursively indenting the main lines.
    """
    fig, ax = setup_ax()

    # We will draw a main concentric set, and 6 smaller sets around the perimeter
    centers = [(50.0, 50.0)]
    radii_max = [45.0]
    
    # Add sub-centers
    n_subs = 6
    for i in range(n_subs):
        angle = i * (2 * np.pi / n_subs)
        sub_cx = 50.0 + 45.0 * np.cos(angle)
        sub_cy = 50.0 + 45.0 * np.sin(angle)
        centers.append((sub_cx, sub_cy))
        radii_max.append(18.0)
        
    n_circles = 30

    # Draw using a scalar field approach (metaballs/distance field) to perfectly merge them
    # Since drawing overlapping circles is messy, we evaluate a field and contour it.
    
    x = np.linspace(-10, 110, 800)
    y = np.linspace(-10, 110, 800)
    X, Y = np.meshgrid(x, y)
    
    field = np.zeros_like(X)
    
    # Main center field
    D_main = np.sqrt((X - centers[0][0])**2 + (Y - centers[0][1])**2)
    # Oscillating field for concentric rings
    field += np.cos(D_main * 1.5) * 1.0
    
    # Sub-centers field
    for i in range(1, len(centers)):
        cx, cy = centers[i]
        D_sub = np.sqrt((X - cx)**2 + (Y - cy)**2)
        # Add localized ripples
        envelope = np.exp(-D_sub**2 / 200.0)
        field += np.cos(D_sub * 2.5) * envelope * 1.5
        
    # Contour plot extracts the concentric lines beautifully
    ax.contour(X, Y, field, levels=15, colors="black", linewidths=1.2)

    save(fig, "abstract concentric fractal recursive subcenter pattern black white texture")


if __name__ == "__main__":
    draw()
