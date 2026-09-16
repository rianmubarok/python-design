import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-60, 60)
    ax.set_ylim(-60, 60)
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


def abstract_opart_tunnel_depth_vortex_illusion_pattern_black_white_texture():
    """Generates a twisting spiral vortex tunnel giving an illusion of deep 3D perspective."""
    fig, ax = setup_ax()
    
    n_steps = 70
    size = 55.0
    angle = 0.0
    
    for i in range(n_steps):
        if size <= 0.5:
            break
            
        # Vertices of a square
        square = np.array([
            [-size, -size],
            [size, -size],
            [size, size],
            [-size, size]
        ])
        
        # Rotate square
        rot_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        
        rotated_square = square @ rot_matrix.T
        
        # Draw outline
        poly = Polygon(rotated_square, fill=False, edgecolor="black", linewidth=0.6 + 1.2 * (i / n_steps))
        ax.add_patch(poly)
        
        # Shrink size and increment angle slightly for twisting vortex effect
        size *= 0.94
        angle += 0.08

    save(fig, "abstract opart tunnel depth vortex illusion pattern black white texture")


if __name__ == "__main__":
    abstract_opart_tunnel_depth_vortex_illusion_pattern_black_white_texture()
