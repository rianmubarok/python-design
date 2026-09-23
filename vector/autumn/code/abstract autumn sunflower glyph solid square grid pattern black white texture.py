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

def draw_sunflower_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    
    # Outer petal silhouette (Solid black)
    t = np.linspace(0, 2*np.pi, 200)
    # Using a frequency of ~16 petals
    r_petals = 0.8 + 0.2 * np.abs(np.sin(16 * t/2))**1.5
    x = r_petals * np.cos(t)
    y = r_petals * np.sin(t)
    ax.fill(x, y, color="black", edgecolor="none", transform=trans, zorder=2)
    
    # White detail: lines separating petals
    for a in np.linspace(0, 2*np.pi, 16, endpoint=False):
        ax.plot([0.3*np.cos(a), 0.95*np.cos(a)], [0.3*np.sin(a), 0.95*np.sin(a)], color="white", lw=size*0.04, transform=trans, zorder=3)
        
    # White detail: Center seed texture (crosshatch)
    ax.add_patch(patches.Circle((0,0), 0.45, facecolor="black", edgecolor="white", lw=size*0.08, transform=trans, zorder=4))
    for v in np.linspace(-0.35, 0.35, 5):
        ax.plot([v, v], [-0.3, 0.3], color="white", lw=size*0.02, transform=trans, zorder=5)
        ax.plot([-0.3, 0.3], [v, v], color="white", lw=size*0.02, transform=trans, zorder=5)

def main():
    fig, ax = setup_ax()
    
    # Packed Square Grid
    cols = 9; rows = 9
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    for i in range(-2, cols+3):
        for j in range(-2, rows+3):
            cx = i * spacing_x
            cy = j * spacing_y
            draw_sunflower_detailed(ax, cx, cy, size=4.8)
            
    save(fig, "abstract autumn sunflower glyph solid square grid pattern black white texture")

if __name__ == "__main__":
    main()
