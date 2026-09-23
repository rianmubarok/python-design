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

def draw_pumpkin_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    ax.add_patch(patches.Ellipse((0, 0), 1.6, 1.2, facecolor="black", edgecolor="none", transform=trans, zorder=2))
    t = np.linspace(-0.6, 0.6, 30)
    ax.plot(-0.4 + 0.1*t**2, t, color="white", lw=size*0.15, transform=trans, zorder=3)
    ax.plot(0.4 - 0.1*t**2, t, color="white", lw=size*0.15, transform=trans, zorder=3)
    ax.plot(np.zeros_like(t), t, color="white", lw=size*0.15, transform=trans, zorder=3)
    stem_pts = [(-0.1, 0.55), (0.1, 0.55), (0.2, 0.9), (0.0, 1.0)]
    stem_codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.LINETO]
    ax.add_patch(patches.PathPatch(Path(stem_pts, stem_codes), facecolor="black", edgecolor="none", transform=trans, zorder=1))

def draw_wheat_detailed(ax, cx, cy, size, angle):
    rad = np.deg2rad(angle)
    trans = transforms.Affine2D().scale(size).rotate(rad).translate(cx, cy) + ax.transData
    ax.plot([0, 0], [-0.8, 0.8], color="black", lw=size*0.3, solid_capstyle="round", transform=trans, zorder=2)
    ax.plot([0, 0], [-0.7, 0.7], color="white", lw=size*0.1, solid_capstyle="round", transform=trans, zorder=3)
    for yk in np.linspace(-0.4, 0.6, 6):
        kx = [-0.1, -0.4, -0.4, -0.1]
        ky = [yk, yk+0.1, yk+0.3, yk+0.1]
        ax.fill(kx, ky, color="black", edgecolor="none", transform=trans, zorder=2)
        kx2 = [0.1, 0.4, 0.4, 0.1]
        ax.fill(kx2, ky, color="black", edgecolor="none", transform=trans, zorder=2)
        ax.plot([-0.25, -0.35], [yk+0.1, yk+0.2], color="white", lw=size*0.06, transform=trans, zorder=3)
        ax.plot([0.25, 0.35], [yk+0.1, yk+0.2], color="white", lw=size*0.06, transform=trans, zorder=3)

def main():
    fig, ax = setup_ax()
    cols = 8; rows = 8
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    for i in range(-2, cols+3):
        for j in range(-2, rows+3):
            cx = i * spacing_x
            cy = j * spacing_y
            
            if (i + j) % 2 == 0:
                draw_pumpkin_detailed(ax, cx, cy, size=4.0)
            else:
                angle = 45 if j % 2 == 0 else -45
                draw_wheat_detailed(ax, cx, cy, size=4.0, angle=angle)
                
    save(fig, "abstract autumn pumpkin wheat glyph solid checkerboard grid pattern black white texture")

if __name__ == "__main__":
    main()
