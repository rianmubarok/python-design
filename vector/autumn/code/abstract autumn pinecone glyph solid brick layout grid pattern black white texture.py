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

def draw_pinecone_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    
    # Base ovate/teardrop shape for pinecone, properly centered visually
    t = np.linspace(0, 2*np.pi, 80)
    # Tear drop centered
    x = 0.5 * np.cos(t)
    y = 0.7 * np.sin(t) - 0.2 * np.sin(t)**2
    # Adjust Y to visually center at (0,0)
    y_offset = (np.max(y) + np.min(y)) / 2
    y -= y_offset
    
    x += 0.04 * np.cos(10*t)
    y += 0.04 * np.sin(10*t)
    
    # Solid black base
    ax.fill(x, y, color="black", edgecolor="none", transform=trans, zorder=2)
    
    # White scale lines (cutouts)
    for ry in np.linspace(-0.6, 0.6, 6):
        w = 0.4 * (1 - abs(ry))
        curve_t = np.linspace(-w, w, 20)
        curve_y = ry - 0.1 * (curve_t / w)**2
        ax.plot(curve_t, curve_y, color="white", lw=size*0.15, transform=trans, zorder=3)
        ax.plot(curve_t - w*0.5, curve_y + 0.1, color="white", lw=size*0.15, transform=trans, zorder=3)
        ax.plot(curve_t + w*0.5, curve_y + 0.1, color="white", lw=size*0.15, transform=trans, zorder=3)

def main():
    fig, ax = setup_ax()
    
    # Brick repeat (Horizontal Stagger) perfectly seamless
    cols = 8; rows = 10
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    # Loop from -2 to cols+2 to cover 0 and 100 boundaries seamlessly
    for j in range(-2, rows+3):
        for i in range(-2, cols+3):
            cx = i * spacing_x
            cy = j * spacing_y
            # Offset every other row
            if j % 2 != 0:
                cx += spacing_x / 2
            draw_pinecone_detailed(ax, cx, cy, size=6.0)
            
    save(fig, "abstract autumn pinecone glyph solid brick layout grid pattern black white texture")

if __name__ == "__main__":
    main()
