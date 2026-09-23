import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.transforms as transforms
from pathlib import Path as FilePath
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")
SCRIPT_DIR = FilePath(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"; SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True); SVG_DIR.mkdir(parents=True, exist_ok=True)

def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
    fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
    ax.set_facecolor("white"); ax.set_xlim(0,100); ax.set_ylim(0,100)
    ax.set_aspect("equal"); ax.axis("off")
    return fig, ax

def save(fig, name):
    fig.savefig(JPG_DIR/f"{name} {DATE}.jpg", dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(SVG_DIR/f"{name} {DATE}.svg", format="svg", pad_inches=0, facecolor="white")
    plt.close(fig); print(f"Saved: {name}")

def draw_scarecrow_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    
    # Redesigned Scarecrow: more robust and textured
    # Base Stick
    ax.plot([0, 0], [-1.0, -0.4], color="black", lw=size*0.1, solid_capstyle="round", transform=trans, zorder=1)
    
    # Shirt Torso (blocky)
    ax.fill([-0.4, 0.4, 0.3, -0.3], [-0.4, -0.4, 0.2, 0.2], color="black", edgecolor="none", transform=trans, zorder=2)
    # Flannel/Shirt pattern (white crosshatch)
    ax.plot([-0.2, -0.2], [-0.3, 0.1], color="white", lw=size*0.02, transform=trans, zorder=3)
    ax.plot([0.2, 0.2], [-0.3, 0.1], color="white", lw=size*0.02, transform=trans, zorder=3)
    ax.plot([-0.3, 0.3], [-0.1, -0.1], color="white", lw=size*0.02, transform=trans, zorder=3)
    
    # Arms sticking out horizontally with straw poking out
    ax.plot([-0.7, -0.3], [0.1, 0.1], color="black", lw=size*0.15, solid_capstyle="round", transform=trans, zorder=1)
    ax.plot([0.7, 0.3], [0.1, 0.1], color="black", lw=size*0.15, solid_capstyle="round", transform=trans, zorder=1)
    # Straw details
    for dx in [-0.8, -0.75, -0.7]:
        ax.plot([dx, dx-0.1], [0.1, 0.0], color="black", lw=size*0.04, transform=trans, zorder=0)
    for dx in [0.8, 0.75, 0.7]:
        ax.plot([dx, dx+0.1], [0.1, 0.0], color="black", lw=size*0.04, transform=trans, zorder=0)

    # Collar / Scarf
    ax.fill([-0.2, 0.2, 0], [0.15, 0.15, -0.1], color="white", edgecolor="black", lw=size*0.04, transform=trans, zorder=4)
    
    # Burlap sack Head
    ax.add_patch(patches.FancyBboxPatch((-0.2, 0.2), 0.4, 0.4, boxstyle="round,pad=0.05", facecolor="black", edgecolor="none", transform=trans, zorder=5))
    
    # Hat with wide brim
    ax.fill([-0.5, 0.5, 0.4, -0.4], [0.6, 0.6, 0.7, 0.7], color="black", edgecolor="none", transform=trans, zorder=6) # Brim
    ax.fill([-0.3, 0.3, 0.2, -0.1], [0.65, 0.65, 1.0, 0.95], color="black", edgecolor="none", transform=trans, zorder=6) # Top
    # Hat patch
    ax.fill([-0.1, 0.1, 0.05, -0.15], [0.75, 0.7, 0.85, 0.9], color="white", edgecolor="none", transform=trans, zorder=7)
    
    # Face details (eyes & stitched mouth)
    ax.add_patch(patches.Circle((-0.1, 0.45), 0.04, color="white", transform=trans, zorder=7))
    ax.add_patch(patches.Circle((0.1, 0.45), 0.04, color="white", transform=trans, zorder=7))
    # Zigzag mouth
    mx = np.linspace(-0.15, 0.15, 5)
    my = 0.3 + 0.02 * np.array([1, -1, 1, -1, 1])
    ax.plot(mx, my, color="white", lw=size*0.02, transform=trans, zorder=7)

def main():
    fig, ax = setup_ax()
    cols = 9; rows = 9
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    for i in range(-2, cols+3):
        for j in range(-2, rows+3):
            cx = i * spacing_x; cy = j * spacing_y
            draw_scarecrow_detailed(ax, cx, cy, size=4.0)
    save(fig, "abstract autumn scarecrow glyph solid square grid pattern black white texture")

if __name__ == "__main__":
    main()
