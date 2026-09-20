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
    Shape Morphing Transition.
    Concentric shapes that smoothly morph from a circle in the center
    to a square at the outer edges.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_shapes = 40
    max_radius = 65.0
    n_pts = 400

    for i in range(1, n_shapes + 1):
        t_shape = (i - 1) / (n_shapes - 1)  # 0 at center (circle), 1 at edge (square)
        r = max_radius * (i / n_shapes)
        
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        # Circle coordinates
        x_circle = np.cos(angles)
        y_circle = np.sin(angles)
        
        # Square coordinates (normalized to match circle radius conceptually)
        # Using the L-infinity norm for a square
        norm = np.maximum(np.abs(np.cos(angles)), np.abs(np.sin(angles)))
        x_square = np.cos(angles) / norm
        y_square = np.sin(angles) / norm
        
        # Morph interpolation
        x = cx + r * (x_circle * (1 - t_shape) + x_square * t_shape)
        y = cy + r * (y_circle * (1 - t_shape) + y_square * t_shape)
        
        ax.plot(x, y, color="black", linewidth=1.5, solid_capstyle="round", solid_joinstyle="round")

    save(fig, "abstract concentric shapes morphing transition pattern black white texture")


if __name__ == "__main__":
    draw()
