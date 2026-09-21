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
    Perspective 3D Tilt Cylinder.
    Concentric circles projected in 3D perspective, making them ellipses 
    that stack downwards, creating the illusion of a deep cylindrical pit or cone.
    """
    fig, ax = setup_ax()

    cx, cy_base = 50.0, 75.0
    n_circles = 60
    max_radius = 50.0

    for i in range(1, n_circles + 1):
        t = i / n_circles
        r_x = max_radius * t
        r_y = max_radius * t * 0.35  # Squashed for perspective
        
        # Shift y downwards to create depth (closer rings are lower on the screen)
        # Using a non-linear curve so it looks like a deep funnel
        depth = (1 - t) ** 1.5 * 55.0
        cy = cy_base - depth
        
        angles = np.linspace(0, 2 * np.pi, 200)
        x = cx + r_x * np.cos(angles)
        y = cy + r_y * np.sin(angles)
        
        # Thicker lines at the top (outer rim), thinner deep inside the pit
        lw = 0.2 + 2.5 * t
        
        ax.plot(x, y, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract concentric circles perspective 3d tilt funnel pattern black white texture")


if __name__ == "__main__":
    draw()
