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
    Quadtree Random Subdivision.
    A square grid that randomly subdivides its cells into 4 smaller squares,
    recursively, creating a high-tech circuit-like grid of varying densities.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    import matplotlib.patches as patches

    def subdivide_rect(x, y, w, h, depth):
        # Base condition: randomly stop subdividing, or max depth reached
        # Deep cells are more likely to stop subdividing
        prob_stop = 0.1 + (depth * 0.2)
        
        if depth >= 5 or rng.random() < prob_stop:
            # Draw the rectangle
            # Alternating solid blacks and thick outlines for texture
            if rng.random() > 0.8:
                rect = patches.Rectangle((x, y), w, h, linewidth=0, facecolor='black')
            else:
                # Add margin to create a "circuit board" detached look
                margin = min(w, h) * 0.1
                rect = patches.Rectangle((x+margin, y+margin), w-2*margin, h-2*margin, 
                                         linewidth=1.5, edgecolor='black', facecolor='none')
            ax.add_patch(rect)
        else:
            # Subdivide into 4
            hw = w / 2
            hh = h / 2
            subdivide_rect(x, y, hw, hh, depth + 1)
            subdivide_rect(x + hw, y, hw, hh, depth + 1)
            subdivide_rect(x, y + hh, hw, hh, depth + 1)
            subdivide_rect(x + hw, y + hh, hw, hh, depth + 1)

    # Start with a big square covering the viewport
    subdivide_rect(-10, -10, 120, 120, 0)

    save(fig, "abstract grid tessellation quadtree random subdivision pattern black white texture")


if __name__ == "__main__":
    draw()
