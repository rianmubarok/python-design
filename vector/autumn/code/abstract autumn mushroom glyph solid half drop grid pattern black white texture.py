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

def draw_mushroom_glyph(ax, cx, cy, size):
    """Draw a solid mushroom silhouette."""
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    
    # Cap (semi-circle)
    t = np.linspace(0, np.pi, 50)
    cx_cap = 0.8 * np.cos(t)
    cy_cap = 0.6 * np.sin(t) + 0.1
    cx_cap = np.concatenate([[-0.8], cx_cap, [0.8]])
    cy_cap = np.concatenate([[0.1], cy_cap, [0.1]])
    ax.fill(cx_cap, cy_cap, color="black", edgecolor="none", transform=trans, zorder=3)
    
    # Stem
    stem_pts = [(-0.25, 0.1), (-0.2, -0.6), (-0.3, -0.8), (0.3, -0.8), (0.2, -0.6), (0.25, 0.1)]
    stem_codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3, Path.CURVE3]
    stem_path = Path(stem_pts, stem_codes)
    ax.add_patch(patches.PathPatch(stem_path, facecolor="black", edgecolor="none", transform=trans, zorder=2))

def main():
    fig, ax = setup_ax()
    
    # Half-drop repeat (columns staggered by half vertical spacing)
    cols, rows = 11, 11
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    for i in range(-1, cols+1):
        for j in range(-1, rows+1):
            cx = spacing_x/2 + i * spacing_x
            cy = spacing_y/2 + j * spacing_y
            
            # Stagger every other column vertically
            if i % 2 != 0:
                cy += spacing_y / 2
                
            draw_mushroom_glyph(ax, cx, cy, size=3.5)
            
    save(fig, "abstract autumn mushroom glyph solid half drop grid pattern black white texture")

if __name__ == "__main__":
    main()
