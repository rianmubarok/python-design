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

def draw_oak_glyph(ax, cx, cy, size, angle):
    rad = np.deg2rad(angle)
    t = np.linspace(0, 2*np.pi, 200)
    lobes = 6
    r = size * (0.55 + 0.45 * np.abs(np.sin(lobes/2 * t))**0.8) * (0.8 + 0.2*np.cos(t))
    x = r * np.cos(t); y = r * np.sin(t)
    
    xr = x*np.cos(rad) - y*np.sin(rad) + cx
    yr = x*np.sin(rad) + y*np.cos(rad) + cy
    
    ax.fill(xr, yr, color="black", edgecolor="none", zorder=3)
    # Thick short stem
    sx = cx - size * 1.0 * np.cos(rad)
    sy = cy - size * 1.0 * np.sin(rad)
    bx = cx - size * 0.5 * np.cos(rad)
    by = cy - size * 0.5 * np.sin(rad)
    ax.plot([bx, sx], [by, sy], color="black", lw=size*0.4, solid_capstyle="round", zorder=2)

def main():
    fig, ax = setup_ax()
    
    # Mathematical Seamless Hex Grid (Staggered Honeycomb)
    # Harus habis membagi 100 baik secara vertikal maupun horizontal
    cols = 10
    rows = 12 # 100/12 = 8.33 (Mendekati jarak hex ideal yaitu 10*sqrt(3)/2 = 8.66)
    
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    
    # Loop melebihi batas 0-100 agar bagian tepi terpotong dengan mulus (seamless wrap)
    for j in range(-1, rows+2):
        for i in range(-1, cols+2):
            cx = i * spacing_x
            cy = j * spacing_y
            
            # Stagger tiap baris ganjil untuk membentuk pola honeycomb
            if j % 2 != 0:
                cx += spacing_x / 2
                
            draw_oak_glyph(ax, cx, cy, size=3.2, angle=90)
            
    save(fig, "abstract autumn oak leaf glyph solid hex grid pattern black white texture")

if __name__ == "__main__":
    main()
