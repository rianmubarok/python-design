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
    Geometric Mandala.
    Intricate interlocking concentric circles with alternating dash and solid
    patterns, featuring radial wave modulations for a mandala aesthetic.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_circles = 35
    max_radius = 65.0

    for i in range(1, n_circles + 1):
        r_base = max_radius * (i / n_circles)
        
        # Determine the style of the ring based on its index
        mode = i % 4
        
        n_pts = 600
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        if mode == 0:
            # Petal-like wave modulation
            petals = 12
            r = r_base + np.sin(angles * petals) * (2.0 + 0.1 * i)
            ax.plot(cx + r * np.cos(angles), cy + r * np.sin(angles), 
                    color="black", linewidth=1.5, solid_capstyle="round")
        elif mode == 1:
            # Dashed circle
            r = r_base
            ax.plot(cx + r * np.cos(angles), cy + r * np.sin(angles), 
                    color="black", linewidth=2.0, linestyle=(0, (3, 4)))
        elif mode == 2:
            # Zig-zag ring
            zigs = 36
            r = r_base + np.sin(angles * zigs) * 1.5
            ax.plot(cx + r * np.cos(angles), cy + r * np.sin(angles), 
                    color="black", linewidth=1.0)
        else:
            # Plain thick circle
            r = r_base
            ax.plot(cx + r * np.cos(angles), cy + r * np.sin(angles), 
                    color="black", linewidth=3.0)

    save(fig, "abstract concentric geometric mandala intricate pattern black white texture")


if __name__ == "__main__":
    draw()
