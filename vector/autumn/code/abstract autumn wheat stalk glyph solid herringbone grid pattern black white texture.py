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

def draw_wheat_detailed(ax, cx, cy, size, angle):
    rad = np.deg2rad(angle)
    trans = transforms.Affine2D().scale(size).rotate(rad).translate(cx, cy) + ax.transData
    
    # Main stalk (thick line)
    ax.plot([0, 0], [-0.8, 0.8], color="black", lw=size*0.3, solid_capstyle="round", transform=trans, zorder=2)
    
    # White detail line in the center of the stalk
    ax.plot([0, 0], [-0.7, 0.7], color="white", lw=size*0.1, solid_capstyle="round", transform=trans, zorder=3)
    
    # Kernels (solid polygons)
    for yk in np.linspace(-0.4, 0.6, 6):
        # Left kernel
        kx = [-0.1, -0.4, -0.4, -0.1]
        ky = [yk, yk+0.1, yk+0.3, yk+0.1]
        ax.fill(kx, ky, color="black", edgecolor="none", transform=trans, zorder=2)
        # Right kernel
        kx = [0.1, 0.4, 0.4, 0.1]
        ax.fill(kx, ky, color="black", edgecolor="none", transform=trans, zorder=2)
        
        # White detail for kernels
        ax.plot([-0.25, -0.35], [yk+0.1, yk+0.2], color="white", lw=size*0.06, transform=trans, zorder=3)
        ax.plot([0.25, 0.35], [yk+0.1, yk+0.2], color="white", lw=size*0.06, transform=trans, zorder=3)

def main():
    fig, ax = setup_ax()
    
    # Herringbone layout (alternating diagonals)
    cols = 8; rows = 8
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    for i in range(-2, cols*2 + 2):
        for j in range(-2, rows*2 + 2):
            cx = (i * spacing_x) / 2
            cy = (j * spacing_y) / 2
            
            # Checkerboard condition for Herringbone
            if (i + j) % 2 == 0:
                if j % 2 == 0:
                    angle = 45
                else:
                    angle = -45
                draw_wheat_detailed(ax, cx, cy, size=4.5, angle=angle)
            
    save(fig, "abstract autumn wheat stalk glyph solid herringbone grid pattern black white texture")

if __name__ == "__main__":
    main()
