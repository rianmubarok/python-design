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

def draw_kite_detailed(ax, cx, cy, size, angle):
    rad = np.deg2rad(angle)
    trans = transforms.Affine2D().scale(size).rotate(rad).translate(cx, cy) + ax.transData
    
    # Kite diamond
    kx = [0, 0.5, 0, -0.5, 0]
    ky = [0.8, 0.2, -0.8, 0.2, 0.8]
    ax.fill(kx, ky, color="black", edgecolor="none", transform=trans, zorder=2)
    
    # White detail: cross frame
    ax.plot([0, 0], [0.8, -0.8], color="white", lw=size*0.06, transform=trans, zorder=3)
    ax.plot([-0.5, 0.5], [0.2, 0.2], color="white", lw=size*0.06, transform=trans, zorder=3)
    
    # Kite tail (squiggly line)
    tail_t = np.linspace(0, 1, 40)
    tail_y = -0.8 - tail_t * 1.5
    tail_x = 0.15 * np.sin(tail_t * 15)
    ax.plot(tail_x, tail_y, color="black", lw=size*0.08, transform=trans, zorder=1)
    
    # Bows on tail
    for by in [0.25, 0.6, 0.9]:
        idx = int(by * 40)
        bx, by_coord = tail_x[idx], tail_y[idx]
        bow_x = [bx-0.15, bx, bx+0.15, bx, bx-0.15]
        bow_y = [by_coord-0.05, by_coord, by_coord-0.05, by_coord+0.05, by_coord-0.05]
        ax.fill(bow_x, bow_y, color="black", edgecolor="none", transform=trans, zorder=2)

def main():
    fig, ax = setup_ax()
    
    # Alternate rotate grid
    cols = 8; rows = 8
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    for i in range(-2, cols+3):
        for j in range(-2, rows+3):
            cx = i * spacing_x
            cy = j * spacing_y
            
            # Rotation checkerboard
            if (i + j) % 2 == 0:
                angle = 15
            else:
                angle = -15
                
            draw_kite_detailed(ax, cx, cy, size=4.5, angle=angle)
            
    save(fig, "abstract autumn kite glyph solid alternate rotate grid pattern black white texture")

if __name__ == "__main__":
    main()
