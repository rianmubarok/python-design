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
    Sierpinski Triangle Recursive Grid.
    A fractal tessellation based on subdividing an equilateral triangle.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches

    def sierpinski(A, B, C, depth):
        if depth == 0:
            # Base case: draw the filled triangle
            poly = patches.Polygon([A, B, C], closed=True, 
                                  facecolor='black', edgecolor='none')
            ax.add_patch(poly)
        else:
            # Find midpoints
            AB = (A + B) / 2
            BC = (B + C) / 2
            CA = (C + A) / 2
            
            # Recursively call for the 3 outer triangles
            sierpinski(A, AB, CA, depth - 1)
            sierpinski(AB, B, BC, depth - 1)
            sierpinski(CA, BC, C, depth - 1)

    # Initial huge triangle that covers the viewport
    side = 140.0
    h = side * np.sqrt(3) / 2
    
    # We'll tile a few of them to make a continuous grid pattern across the screen
    for col in range(-1, 3):
        for row in range(-1, 2):
            cx = col * side - (side/2 if row % 2 != 0 else 0)
            cy = row * h - 10
            
            # Pointing Up
            A = np.array([cx, cy])
            B = np.array([cx + side, cy])
            C = np.array([cx + side/2, cy + h])
            sierpinski(A, B, C, 6)
            
            # Pointing Down (to fill gaps)
            A_down = np.array([cx + side/2, cy + h])
            B_down = np.array([cx + side*1.5, cy + h])
            C_down = np.array([cx + side, cy])
            sierpinski(A_down, B_down, C_down, 6)

    save(fig, "abstract grid tessellation sierpinski triangle recursive pattern black white texture")


if __name__ == "__main__":
    draw()
