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

def draw_maple_glyph(ax, cx, cy, size, angle):
    """Draw a solid, bold maple leaf silhouette (glyph style)."""
    rad = np.deg2rad(angle)
    trans = transforms.Affine2D().scale(size).rotate(rad).translate(cx, cy) + ax.transData
    
    # Precise maple leaf path - outer contour only
    pts = [
        (0.0, -0.9), (0.04, -0.3), (0.25, -0.45), (0.35, -0.3), (0.22, -0.1),
        (0.75, -0.15), (0.85, 0.1), (0.55, 0.2), (0.75, 0.45), (0.55, 0.45), (0.4, 0.3),
        (0.45, 0.75), (0.25, 0.65), (0.0, 1.0),
        (-0.25, 0.65), (-0.45, 0.75), (-0.4, 0.3), (-0.55, 0.45), (-0.75, 0.45),
        (-0.55, 0.2), (-0.85, 0.1), (-0.75, -0.15), (-0.22, -0.1), (-0.35, -0.3),
        (-0.25, -0.45), (-0.04, -0.3), (0.0, -0.9)
    ]
    codes = [Path.MOVETO] + [Path.LINETO]*(len(pts)-2) + [Path.CLOSEPOLY]
    
    path = Path(pts, codes)
    # Glyph style: purely solid black fill, no outline
    patch = patches.PathPatch(path, facecolor="black", edgecolor="none", transform=trans, zorder=3)
    ax.add_patch(patch)

def main():
    fig, ax = setup_ax()
    
    # Simple uniform grid layout
    cols = 8
    rows = 8
    spacing = 100 / cols
    
    # Margin offset so the grid is perfectly centered and seamless-ready
    offset = spacing / 2
    
    for i in range(cols):
        for j in range(rows):
            cx = offset + i * spacing
            cy = offset + j * spacing
            
            # Simple alternating rotation (grid rotate pattern)
            if (i + j) % 2 == 0:
                angle = 45
            else:
                angle = -45
                
            draw_maple_glyph(ax, cx, cy, size=4.5, angle=angle)
            
    save(fig, "abstract autumn maple leaf glyph solid grid rotate pattern black white texture")

if __name__ == "__main__":
    main()
