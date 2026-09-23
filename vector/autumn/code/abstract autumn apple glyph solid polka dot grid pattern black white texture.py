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

def draw_apple_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    
    # Apple body (heart-ish rounded shape)
    t = np.linspace(0, 2*np.pi, 100)
    x = 0.8 * np.cos(t)
    y = 0.7 * np.sin(t) - 0.1 * np.cos(2*t) - 0.1 * np.cos(t)
    
    # Center geometrically
    y_cent = y - (np.max(y) + np.min(y))/2
    
    ax.fill(x, y_cent, color="black", edgecolor="none", transform=trans, zorder=2)
    
    # White detail: crescent highlight
    ht = np.linspace(-np.pi*0.2, np.pi*0.4, 20)
    hx = 0.55 * np.cos(ht) - 0.15
    hy = 0.55 * np.sin(ht) + 0.1 - (np.max(y) + np.min(y))/2
    ax.plot(hx, hy, color="white", lw=size*0.12, transform=trans, zorder=3)
    
    # Stem
    ax.plot([0, 0.15], [0.6, 1.0], color="black", lw=size*0.15, transform=trans, zorder=1)
    # Small leaf attached to stem
    ax.fill([0.15, 0.4, 0.5, 0.2], [0.7, 0.75, 0.95, 0.9], color="black", edgecolor="none", transform=trans, zorder=2)
    ax.plot([0.15, 0.5], [0.7, 0.95], color="white", lw=size*0.06, transform=trans, zorder=3)

def main():
    fig, ax = setup_ax()
    
    # Simple Polka Dot Square Grid
    cols = 9; rows = 9
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    for i in range(-1, cols+2):
        for j in range(-1, rows+2):
            cx = i * spacing_x
            cy = j * spacing_y
            draw_apple_detailed(ax, cx, cy, size=4.5)
            
    save(fig, "abstract autumn apple glyph solid polka dot grid pattern black white texture")

if __name__ == "__main__":
    main()
