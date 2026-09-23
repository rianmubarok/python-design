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

def draw_umbrella_detailed(ax, cx, cy, size, angle):
    rad = np.deg2rad(angle)
    trans = transforms.Affine2D().scale(size).rotate(rad).translate(cx, cy) + ax.transData
    
    # Canopy (Semi circle with scalloped edge)
    t = np.linspace(0, np.pi, 100)
    cx_top = 0.8 * np.cos(t)
    cy_top = 0.8 * np.sin(t)
    
    # Scalloped bottom edge
    st = np.linspace(-0.8, 0.8, 100)
    # create 4 scallops
    cy_bottom = 0.15 * np.abs(np.sin(st * np.pi / 0.4))
    
    x_poly = np.concatenate([cx_top, st[::-1]])
    y_poly = np.concatenate([cy_top, cy_bottom[::-1]])
    
    # Center object geometrically
    y_cent = y_poly - 0.4
    
    ax.fill(x_poly, y_cent, color="black", edgecolor="none", transform=trans, zorder=2)
    
    # White detail panel lines
    ax.plot([-0.4, 0.0], [0.15-0.4, 0.8-0.4], color="white", lw=size*0.06, transform=trans, zorder=3)
    ax.plot([0.4, 0.0], [0.15-0.4, 0.8-0.4], color="white", lw=size*0.06, transform=trans, zorder=3)
    
    # Handle (J shape)
    hx = np.linspace(0, 0.15, 20)
    hy = -0.5 - 0.15*np.cos(np.linspace(0, np.pi, 20)) - 0.4
    ax.plot([0, 0], [0.0-0.4, -0.65-0.4], color="black", lw=size*0.08, transform=trans, zorder=1)
    
    # J hook
    t_hook = np.linspace(np.pi, 2*np.pi, 20)
    ax.plot(0.15 + 0.15*np.cos(t_hook), -0.65-0.4 + 0.15*np.sin(t_hook), color="black", lw=size*0.08, transform=trans, zorder=1)
    
    # Top tip
    ax.plot([0, 0], [0.8-0.4, 0.95-0.4], color="black", lw=size*0.08, transform=trans, zorder=1)

def main():
    fig, ax = setup_ax()
    
    # Offset Drop Grid (Rain pattern)
    cols = 8; rows = 10
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    for i in range(-2, cols+3):
        for j in range(-2, rows+3):
            cx = i * spacing_x
            cy = j * spacing_y
            
            # Stagger rows and slight alternating tilt
            if j % 2 != 0:
                cx += spacing_x / 2
                angle = -15
            else:
                angle = 15
                
            draw_umbrella_detailed(ax, cx, cy, size=4.5, angle=angle)
            
    save(fig, "abstract autumn umbrella glyph solid offset drop grid pattern black white texture")

if __name__ == "__main__":
    main()
