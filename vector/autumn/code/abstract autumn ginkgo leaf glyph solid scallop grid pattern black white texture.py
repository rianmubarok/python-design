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

def draw_ginkgo_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    
    # Ginkgo fan shape
    t1 = np.linspace(-np.pi*0.4, -0.05, 30)
    t2 = np.linspace(0.05, np.pi*0.4, 30)
    
    x_fan1 = 0.85 * np.sin(t1); y_fan1 = 0.85 * np.cos(t1)
    x_fan2 = 0.85 * np.sin(t2); y_fan2 = 0.85 * np.cos(t2)
    
    x_raw = np.concatenate([[0.0, -0.02], x_fan1, [0.0], x_fan2, [0.02, 0.0]])
    y_raw = np.concatenate([[-0.8, -0.1], y_fan1, [0.65], y_fan2, [-0.1, -0.8]])
    
    # Center mathematically
    y_offset = (np.max(y_raw) + np.min(y_raw)) / 2
    y_cent = y_raw - y_offset
    
    ax.fill(x_raw, y_cent, color="black", edgecolor="none", transform=trans, zorder=2)
    
    # White detail lines (veins radiating from stem)
    for a in np.linspace(-np.pi*0.3, np.pi*0.3, 7):
        if abs(a) < 0.1: continue # skip middle notch
        r = np.linspace(0.1, 0.75, 10)
        vx = r * np.sin(a)
        vy = r * np.cos(a) - y_offset
        ax.plot(vx, vy, color="white", lw=size*0.08, transform=trans, zorder=3)

def main():
    fig, ax = setup_ax()
    
    # Scallop / overlapping scales grid
    cols = 10; rows = 16
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    for j in range(-2, rows+3):
        for i in range(-2, cols+3):
            cx = i * spacing_x
            cy = j * spacing_y
            if j % 2 != 0:
                cx += spacing_x / 2
            draw_ginkgo_detailed(ax, cx, cy, size=7.0) # slightly oversized to create overlap/scallop feel
            
    save(fig, "abstract autumn ginkgo leaf glyph solid scallop grid pattern black white texture")

if __name__ == "__main__":
    main()
