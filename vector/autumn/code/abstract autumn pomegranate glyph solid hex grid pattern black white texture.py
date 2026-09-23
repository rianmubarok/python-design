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

def draw_pomegranate_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    
    # Body (circle slightly flattened at top/bottom)
    t = np.linspace(0, 2*np.pi, 80)
    x = 0.7 * np.cos(t)
    y = 0.65 * np.sin(t) - 0.05*np.cos(2*t)
    
    y_cent = y - (np.max(y) + np.min(y))/2
    
    # Crown (top spiky bits)
    crown_x = [-0.15, -0.2, -0.05, 0, 0.05, 0.2, 0.15]
    crown_y = [0.6, 0.85, 0.7, 0.9, 0.7, 0.85, 0.6]
    crown_y_cent = np.array(crown_y) - (np.max(y) + np.min(y))/2
    
    ax.fill(x, y_cent, color="black", edgecolor="none", transform=trans, zorder=2)
    ax.fill(crown_x, crown_y_cent, color="black", edgecolor="none", transform=trans, zorder=2)
    
    # White detail: Seed crack (crescent cut-out showing seeds)
    cx_cut = 0.2 + 0.2*np.cos(t)
    cy_cut = 0.2*np.sin(t) - (np.max(y) + np.min(y))/2
    ax.fill(cx_cut, cy_cut, color="white", edgecolor="none", transform=trans, zorder=3)
    
    # Seeds (black dots inside the white cut-out)
    for sx, sy in [(0.15, 0.05), (0.25, 0.1), (0.18, -0.1), (0.28, -0.05), (0.3, 0.05)]:
        ax.add_patch(patches.Circle((sx, sy - (np.max(y) + np.min(y))/2), 0.04, color="black", transform=trans, zorder=4))
        
    # Contour line
    ax.plot([-0.5, -0.2], [-0.3, -0.5], color="white", lw=size*0.06, transform=trans, zorder=3)

def main():
    fig, ax = setup_ax()
    
    # Hex grid
    cols = 10; rows = 12
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    for i in range(-2, cols+3):
        for j in range(-2, rows+3):
            cx = i * spacing_x
            cy = j * spacing_y
            if j % 2 != 0:
                cx += spacing_x / 2
                
            draw_pomegranate_detailed(ax, cx, cy, size=4.5)
            
    save(fig, "abstract autumn pomegranate glyph solid hex grid pattern black white texture")

if __name__ == "__main__":
    main()
