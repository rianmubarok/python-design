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

def draw_acorn_glyph(ax, cx, cy, size, angle):
    """Draw a solid acorn silhouette with a tiny white gap to separate the cap."""
    rad = np.deg2rad(angle)
    trans = transforms.Affine2D().scale(size).rotate(rad).translate(cx, cy) + ax.transData
    
    # Body (lower half)
    body_pts = [(-0.4, 0.05), (-0.4, -0.3), (-0.2, -0.7), (0.0, -0.9), (0.2, -0.7), (0.4, -0.3), (0.4, 0.05)]
    body_codes = [Path.MOVETO] + [Path.CURVE4]*(len(body_pts)-1)
    body_path = Path(body_pts, body_codes)
    ax.add_patch(patches.PathPatch(body_path, facecolor="black", edgecolor="none", transform=trans, zorder=2))
    
    # Cap (upper half)
    cap_pts = [(-0.5, 0.1), (-0.4, 0.5), (-0.2, 0.6), (0.0, 0.6), (0.2, 0.6), (0.4, 0.5), (0.5, 0.1), (-0.5, 0.1)]
    cap_codes = [Path.MOVETO] + [Path.LINETO]*(len(cap_pts)-2) + [Path.CLOSEPOLY]
    cap_path = Path(cap_pts, cap_codes)
    ax.add_patch(patches.PathPatch(cap_path, facecolor="black", edgecolor="none", transform=trans, zorder=2))
    
    # Tiny stem
    stem = plt.Line2D([0, 0], [0.6, 0.85], color="black", lw=size*0.3)
    stem.set_transform(trans)
    ax.add_line(stem)

def main():
    fig, ax = setup_ax()
    
    cols, rows = 9, 9
    spacing = 100 / cols
    offset = spacing / 2
    
    for i in range(cols):
        for j in range(rows):
            cx = offset + i * spacing
            cy = offset + j * spacing
            
            # Alternating upright and upside down
            if (i + j) % 2 == 0:
                angle = 0
            else:
                angle = 180
                
            draw_acorn_glyph(ax, cx, cy, size=4.0, angle=angle)
            
    save(fig, "abstract autumn acorn glyph solid checkerboard grid pattern black white texture")

if __name__ == "__main__":
    main()
