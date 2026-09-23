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

def draw_corncob_detailed(ax, cx, cy, size, angle):
    rad = np.deg2rad(angle)
    trans = transforms.Affine2D().scale(size).rotate(rad).translate(cx, cy) + ax.transData
    
    # Corncob body
    t = np.linspace(0, 2*np.pi, 60)
    x = 0.25 * np.cos(t)
    y = 0.6 * np.sin(t)
    ax.fill(x, y, color="black", edgecolor="none", transform=trans, zorder=2)
    
    # White kernel grid lines
    for lx in np.linspace(-0.15, 0.15, 3):
        ax.plot([lx, lx], [-0.5, 0.5], color="white", lw=size*0.03, transform=trans, zorder=3)
    for ly in np.linspace(-0.4, 0.4, 6):
        ax.plot([-0.2, 0.2], [ly, ly], color="white", lw=size*0.03, transform=trans, zorder=3)
        
    # Peeling husk leaves
    # Left husk
    ax.fill([-0.1, -0.4, -0.5, -0.1], [-0.4, -0.1, -0.4, -0.6], color="black", edgecolor="none", transform=trans, zorder=1)
    ax.plot([-0.1, -0.4], [-0.4, -0.3], color="white", lw=size*0.04, transform=trans, zorder=3)
    # Right husk
    ax.fill([0.1, 0.4, 0.5, 0.1], [-0.4, -0.1, -0.4, -0.6], color="black", edgecolor="none", transform=trans, zorder=1)
    ax.plot([0.1, 0.4], [-0.4, -0.3], color="white", lw=size*0.04, transform=trans, zorder=3)

def main():
    fig, ax = setup_ax()
    
    # Basketweave Grid (Alternating orthogonal directions)
    cols = 8; rows = 8
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    for i in range(-2, cols+3):
        for j in range(-2, rows+3):
            cx = i * spacing_x
            cy = j * spacing_y
            
            # Alternate angle based on parity of sum
            if (i + j) % 2 == 0:
                angle = 0
            else:
                angle = 90
            
            # Draw double objects to simulate basketweave blocks
            if angle == 0:
                draw_corncob_detailed(ax, cx - spacing_x*0.15, cy, size=5.0, angle=angle)
                draw_corncob_detailed(ax, cx + spacing_x*0.15, cy, size=5.0, angle=angle)
            else:
                draw_corncob_detailed(ax, cx, cy - spacing_y*0.15, size=5.0, angle=angle)
                draw_corncob_detailed(ax, cx, cy + spacing_y*0.15, size=5.0, angle=angle)
                
    save(fig, "abstract autumn corncob glyph solid basketweave grid pattern black white texture")

if __name__ == "__main__":
    main()
