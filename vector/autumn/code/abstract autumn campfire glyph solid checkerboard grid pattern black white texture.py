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

def draw_campfire_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    
    # Crossed logs (rounded rectangles represented by thick lines)
    ax.plot([-0.5, 0.5], [-0.5, -0.2], color="black", lw=size*0.2, solid_capstyle="round", transform=trans, zorder=1)
    ax.plot([0.5, -0.5], [-0.5, -0.2], color="black", lw=size*0.2, solid_capstyle="round", transform=trans, zorder=2)
    
    # White detail: bark lines on logs
    ax.plot([-0.3, 0.3], [-0.4, -0.25], color="white", lw=size*0.04, transform=trans, zorder=3)
    ax.plot([0.3, -0.3], [-0.4, -0.25], color="white", lw=size*0.04, transform=trans, zorder=3)
    
    # Flame (teardrop with points)
    fx = [0, 0.4, 0.6, 0, -0.6, -0.4, 0]
    fy = [0.8, 0.1, -0.3, -0.4, -0.3, 0.1, 0.8]
    # Smooth flame body using spline or many points
    t = np.linspace(0, 2*np.pi, 80)
    flame_x = 0.5 * np.cos(t) * (1 - 0.3*np.sin(t))
    flame_y = 0.5 * np.sin(t) - 0.2*np.cos(2*t) + 0.1
    ax.fill(flame_x, flame_y, color="black", edgecolor="none", transform=trans, zorder=4)
    
    # White detail: inner flame
    inner_t = np.linspace(0, 2*np.pi, 60)
    inner_x = 0.2 * np.cos(inner_t) * (1 - 0.3*np.sin(inner_t))
    inner_y = 0.2 * np.sin(inner_t) - 0.1*np.cos(2*inner_t) - 0.05
    ax.plot(inner_x, inner_y, color="white", lw=size*0.06, transform=trans, zorder=5)
    
    # Sparks (dots)
    ax.add_patch(patches.Circle((0.3, 0.7), 0.04, color="black", transform=trans, zorder=6))
    ax.add_patch(patches.Circle((-0.2, 0.9), 0.04, color="black", transform=trans, zorder=6))

def main():
    fig, ax = setup_ax()
    
    # Checkerboard grid
    cols = 10; rows = 10
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    for i in range(-2, cols+3):
        for j in range(-2, rows+3):
            # Checkerboard condition
            if (i + j) % 2 == 0:
                cx = i * spacing_x
                cy = j * spacing_y
                draw_campfire_detailed(ax, cx, cy, size=4.5)
            
    save(fig, "abstract autumn campfire glyph solid checkerboard grid pattern black white texture")

if __name__ == "__main__":
    main()
