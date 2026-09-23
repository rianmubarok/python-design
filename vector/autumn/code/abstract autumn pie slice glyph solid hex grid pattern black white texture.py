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

def draw_pie_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    
    # Slice triangle shape (viewed from above/slight angle)
    px = [0, 0.6, -0.6, 0]
    py = [-0.6, 0.4, 0.4, -0.6]
    ax.fill(px, py, color="black", edgecolor="none", transform=trans, zorder=2)
    
    # Thick scalloped crust at the back
    crust_t = np.linspace(-0.65, 0.65, 50)
    crust_y = 0.4 + 0.1 * np.abs(np.sin(crust_t * 5 * np.pi / 0.65))
    ax.fill(np.concatenate([crust_t, crust_t[::-1]]), 
            np.concatenate([crust_y, np.full_like(crust_t, 0.3)]), 
            color="black", edgecolor="none", transform=trans, zorder=3)
            
    # White detail: lattice / cuts on the top crust
    ax.plot([0, 0.3], [0, 0.3], color="white", lw=size*0.06, transform=trans, zorder=4)
    ax.plot([0, -0.3], [0, 0.3], color="white", lw=size*0.06, transform=trans, zorder=4)
    ax.plot([-0.2, 0.2], [0.1, 0.1], color="white", lw=size*0.06, transform=trans, zorder=4)
    
    # Steam
    st = np.linspace(0, 1, 20)
    ax.plot(-0.2 + 0.05*np.sin(st*10), 0.5 + 0.3*st, color="black", lw=size*0.06, transform=trans, zorder=1)
    ax.plot(0.2 + 0.05*np.sin(st*10 + 2), 0.5 + 0.3*st, color="black", lw=size*0.06, transform=trans, zorder=1)

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
                
            draw_pie_detailed(ax, cx, cy, size=4.5)
            
    save(fig, "abstract autumn pie slice glyph solid hex grid pattern black white texture")

if __name__ == "__main__":
    main()
