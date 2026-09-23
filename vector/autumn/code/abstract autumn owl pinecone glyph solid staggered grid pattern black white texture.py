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

def draw_owl_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    
    # Redesigned Owl: Peanut shape body
    t = np.linspace(0, 2*np.pi, 100)
    r = 0.7 * (1 - 0.15*np.cos(2*t)) 
    x = r * np.cos(t)
    y = r * np.sin(t)
    y_cent = y - (np.max(y) + np.min(y))/2
    
    ears_x = [-0.45, -0.6, -0.2, 0.2, 0.6, 0.45]
    ears_y = [0.4, 0.85, 0.5, 0.5, 0.85, 0.4]
    ears_y_cent = np.array(ears_y) - (np.max(y) + np.min(y))/2
    
    ax.fill(x, y_cent, color="black", edgecolor="none", transform=trans, zorder=2)
    ax.fill(ears_x, ears_y_cent, color="black", edgecolor="none", transform=trans, zorder=2)
    
    ax.plot([-0.5, -0.1], [0.55 - np.mean(y), 0.35 - np.mean(y)], color="white", lw=size*0.06, solid_capstyle="round", transform=trans, zorder=3)
    ax.plot([0.5, 0.1], [0.55 - np.mean(y), 0.35 - np.mean(y)], color="white", lw=size*0.06, solid_capstyle="round", transform=trans, zorder=3)
    
    ax.add_patch(patches.Circle((-0.25, 0.2 - np.mean(y)), 0.2, facecolor="white", edgecolor="none", transform=trans, zorder=3))
    ax.add_patch(patches.Circle((0.25, 0.2 - np.mean(y)), 0.2, facecolor="white", edgecolor="none", transform=trans, zorder=3))
    ax.add_patch(patches.Circle((-0.25, 0.2 - np.mean(y)), 0.1, facecolor="black", edgecolor="none", transform=trans, zorder=4))
    ax.add_patch(patches.Circle((0.25, 0.2 - np.mean(y)), 0.1, facecolor="black", edgecolor="none", transform=trans, zorder=4))
    
    bx = [0, 0.1, 0, -0.1]; by = [0.1, 0, -0.2, 0]
    by_cent = np.array(by) - np.mean(y)
    ax.fill(bx, by_cent, color="white", edgecolor="none", transform=trans, zorder=3)
    
    for fy in [-0.2, -0.4, -0.6]:
        ax.plot([-0.2, 0, 0.2], [fy + 0.1 - np.mean(y), fy - np.mean(y), fy + 0.1 - np.mean(y)], color="white", lw=size*0.03, transform=trans, zorder=3)
        
    wt = np.linspace(-np.pi*0.8, -np.pi*0.2, 30)
    wx = 0.5 * np.cos(wt) - 0.1
    wy = 0.5 * np.sin(wt) - 0.2 - np.mean(y)
    ax.plot(wx, wy, color="white", lw=size*0.04, transform=trans, zorder=3)
    ax.plot(-wx, wy, color="white", lw=size*0.04, transform=trans, zorder=3)
    
    ax.plot([-0.2, -0.2], [-0.75 - np.mean(y), -0.9 - np.mean(y)], color="black", lw=size*0.08, transform=trans, zorder=1)
    ax.plot([0.2, 0.2], [-0.75 - np.mean(y), -0.9 - np.mean(y)], color="black", lw=size*0.08, transform=trans, zorder=1)

def draw_pinecone_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    t = np.linspace(0, 2*np.pi, 80)
    x = 0.5 * np.cos(t)
    y = 0.7 * np.sin(t) - 0.2 * np.sin(t)**2
    y -= (np.max(y) + np.min(y)) / 2
    x += 0.04 * np.cos(10*t)
    y += 0.04 * np.sin(10*t)
    ax.fill(x, y, color="black", edgecolor="none", transform=trans, zorder=2)
    for ry in np.linspace(-0.6, 0.6, 6):
        w = 0.4 * (1 - abs(ry))
        curve_t = np.linspace(-w, w, 20)
        curve_y = ry - 0.1 * (curve_t / w)**2
        ax.plot(curve_t, curve_y, color="white", lw=size*0.15, transform=trans, zorder=3)
        ax.plot(curve_t - w*0.5, curve_y + 0.1, color="white", lw=size*0.15, transform=trans, zorder=3)
        ax.plot(curve_t + w*0.5, curve_y + 0.1, color="white", lw=size*0.15, transform=trans, zorder=3)

def main():
    fig, ax = setup_ax()
    cols = 9; rows = 9
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    for i in range(-2, cols+3):
        for j in range(-2, rows+3):
            cx = i * spacing_x; cy = j * spacing_y
            if j % 2 != 0: cx += spacing_x / 2
            if (i + j) % 2 == 0:
                draw_owl_detailed(ax, cx, cy, size=3.5)
            else:
                draw_pinecone_detailed(ax, cx, cy, size=4.5)
    save(fig, "abstract autumn owl pinecone glyph solid staggered grid pattern black white texture")

if __name__ == "__main__":
    main()
