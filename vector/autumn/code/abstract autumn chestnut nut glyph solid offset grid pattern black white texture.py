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

def draw_chestnut_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    
    # Chestnut nut shape (teardrop with flat bottom)
    t = np.linspace(0, 2*np.pi, 80)
    x = 0.5 * np.cos(t)
    y = 0.4 * np.sin(t)
    y = np.where(y < -0.1, -0.1, y) # flatten bottom
    y += 0.3 * np.abs(np.sin(t/2))**3 * (1 if np.mean(np.sin(t)) > 0 else -1)
    
    y_offset = (np.max(y) + np.min(y))/2
    y -= y_offset
    
    # Nut body
    ax.fill(x, y, color="black", edgecolor="none", transform=trans, zorder=2)
    
    # Spiky husk (bottom base)
    st = np.linspace(np.pi*0.8, np.pi*2.2, 30)
    sx = 0.6 * np.cos(st)
    sy = 0.2 * np.sin(st) - 0.15 - y_offset
    sy += 0.1 * np.cos(20*st) # spikes
    ax.fill(np.concatenate([[0], sx, [0]]), np.concatenate([[0], sy, [0]]), color="black", edgecolor="none", transform=trans, zorder=1)
    
    # White highlight on the nut (glossy shine)
    ax.plot([0.1, 0.3], [0.1-y_offset, 0.2-y_offset], color="white", lw=size*0.1, transform=trans, zorder=3)
    ax.plot([0.15, 0.25], [0.05-y_offset, 0.12-y_offset], color="white", lw=size*0.06, transform=trans, zorder=3)

def main():
    fig, ax = setup_ax()
    
    # Offset Grid
    cols = 10; rows = 12
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    for i in range(-2, cols+3):
        for j in range(-2, rows+3):
            cx = i * spacing_x
            cy = j * spacing_y
            if j % 2 != 0:
                cx += spacing_x / 2
            draw_chestnut_detailed(ax, cx, cy, size=5.0)
            
    save(fig, "abstract autumn chestnut nut glyph solid offset grid pattern black white texture")

if __name__ == "__main__":
    main()
