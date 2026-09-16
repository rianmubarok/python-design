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
    Rhombille Tumbling Blocks Illusion.
    A classic geometric tessellation where rhombi cover the plane in 3 different
    orientations, creating an optical illusion of 3D stacked cubes.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches

    scale = 6.0
    h = scale * np.sqrt(3) / 2.0
    
    cols = int(120 / (scale * 1.5)) + 2
    rows = int(120 / h) + 2
    
    # We build the rhombille tiling by drawing 3 rhombi at each node of a hex grid
    # Center node
    center = np.array([0, 0])
    
    # Angles for the 3 points surrounding the center to form a hexagon
    a1 = np.radians(30)
    a2 = np.radians(150)
    a3 = np.radians(270)
    
    p1 = np.array([scale * np.cos(a1), scale * np.sin(a1)])
    p2 = np.array([scale * np.cos(a2), scale * np.sin(a2)])
    p3 = np.array([scale * np.cos(a3), scale * np.sin(a3)])
    
    # The outer points of the rhombi
    po1 = p1 + p2
    po2 = p2 + p3
    po3 = p3 + p1
    
    # The 3 rhombi
    rhombus_top = [center, p1, po1, p2]
    rhombus_left = [center, p2, po2, p3]
    rhombus_right = [center, p3, po3, p1]

    for row in range(-2, rows):
        for col in range(-2, cols):
            cx = col * scale * 1.5
            cy = row * h * 2.0
            if col % 2 != 0:
                cy += h
                
            # Shading styles to emphasize the 3D effect
            style_t = {'facecolor': 'white', 'edgecolor': 'black', 'linewidth': 1.5}
            style_l = {'facecolor': 'none', 'edgecolor': 'black', 'linewidth': 1.5, 'hatch': '////'}
            style_r = {'facecolor': 'black', 'edgecolor': 'black', 'linewidth': 1.5}
            
            rt = patches.Polygon(np.array(rhombus_top) + [cx, cy], closed=True, **style_t)
            rl = patches.Polygon(np.array(rhombus_left) + [cx, cy], closed=True, **style_l)
            rr = patches.Polygon(np.array(rhombus_right) + [cx, cy], closed=True, **style_r)
            
            ax.add_patch(rt)
            ax.add_patch(rl)
            ax.add_patch(rr)

    save(fig, "abstract grid tessellation rhombille tumbling blocks illusion pattern black white texture")


if __name__ == "__main__":
    draw()
