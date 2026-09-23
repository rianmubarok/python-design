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

def draw_teardrop_detailed(ax, cx, cy, size, angle):
    rad = np.deg2rad(angle)
    trans = transforms.Affine2D().scale(size).rotate(rad).translate(cx, cy) + ax.transData
    
    t = np.linspace(0, 2*np.pi, 100)
    r = 0.5 + 0.5 * np.abs(np.sin(t/2))**1.5
    # The mathematical origin is at the tip. We must offset it so it's visually centered.
    x_raw = r * np.cos(t)
    y_raw = r * np.sin(t)
    
    # Center calculation
    x_cent = x_raw - (np.max(x_raw) + np.min(x_raw))/2
    y_cent = y_raw - (np.max(y_raw) + np.min(y_raw))/2
    
    ax.fill(x_cent, y_cent, color="black", edgecolor="none", transform=trans, zorder=2)
    
    # White center vein
    ax.plot([np.min(x_cent)+0.1, np.max(x_cent)-0.2], [0, 0], color="white", lw=size*0.12, transform=trans, zorder=3)
    
    # Stem
    ax.plot([np.min(x_cent), np.min(x_cent)-0.2], [0, 0], color="black", lw=size*0.15, transform=trans, zorder=1)

def main():
    fig, ax = setup_ax()
    
    cols = 12; rows = 14
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    for i in range(-2, cols+3):
        for j in range(-2, rows+3):
            cx = i * spacing_x
            cy = j * spacing_y
            
            if i % 2 != 0:
                cy += spacing_y / 2
                angle = -90
            else:
                angle = 90
                
            draw_teardrop_detailed(ax, cx, cy, size=3.5, angle=angle)
            
    save(fig, "abstract autumn simple leaf glyph solid vertical stripe grid pattern black white texture")

if __name__ == "__main__":
    main()
