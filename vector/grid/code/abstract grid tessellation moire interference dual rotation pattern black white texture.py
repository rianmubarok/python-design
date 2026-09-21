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
    Moire Interference Grid.
    Two dense Cartesian grids rotated slightly out of phase with each other.
    When overlaid, they produce enormous, sweeping Moire interference patterns.
    """
    fig, ax = setup_ax()

    spacing = 0.8
    n_lines = 250
    length = 200.0
    
    # Helper to draw a grid
    def draw_grid(angle, cx, cy):
        rad = np.radians(angle)
        for i in range(-n_lines // 2, n_lines // 2):
            # Local coordinates of line
            # Vertical lines
            lx_v = i * spacing
            p1_v = np.array([lx_v, -length/2])
            p2_v = np.array([lx_v, length/2])
            
            # Horizontal lines
            ly_h = i * spacing
            p1_h = np.array([-length/2, ly_h])
            p2_h = np.array([length/2, ly_h])
            
            # Rotate and translate
            for p1, p2 in [(p1_v, p2_v), (p1_h, p2_h)]:
                rx1 = p1[0] * np.cos(rad) - p1[1] * np.sin(rad) + cx
                ry1 = p1[0] * np.sin(rad) + p1[1] * np.cos(rad) + cy
                rx2 = p2[0] * np.cos(rad) - p2[1] * np.sin(rad) + cx
                ry2 = p2[0] * np.sin(rad) + p2[1] * np.cos(rad) + cy
                
                ax.plot([rx1, rx2], [ry1, ry2], color="black", linewidth=0.3)

    # Grid 1 at 0 degrees
    draw_grid(0.0, 50.0, 50.0)
    
    # Grid 2 rotated slightly by 4.5 degrees
    draw_grid(4.5, 50.0, 50.0)

    save(fig, "abstract grid tessellation moire interference dual rotation pattern black white texture")


if __name__ == "__main__":
    draw()
