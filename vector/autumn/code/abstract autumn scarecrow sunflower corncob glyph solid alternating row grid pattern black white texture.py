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

def draw_scarecrow_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    
    # Base Stick
    ax.plot([0, 0], [-1.0, -0.4], color="black", lw=size*0.1, solid_capstyle="round", transform=trans, zorder=1)
    # Shirt Torso
    ax.fill([-0.4, 0.4, 0.3, -0.3], [-0.4, -0.4, 0.2, 0.2], color="black", edgecolor="none", transform=trans, zorder=2)
    # Flannel/Shirt pattern
    ax.plot([-0.2, -0.2], [-0.3, 0.1], color="white", lw=size*0.02, transform=trans, zorder=3)
    ax.plot([0.2, 0.2], [-0.3, 0.1], color="white", lw=size*0.02, transform=trans, zorder=3)
    ax.plot([-0.3, 0.3], [-0.1, -0.1], color="white", lw=size*0.02, transform=trans, zorder=3)
    # Arms
    ax.plot([-0.7, -0.3], [0.1, 0.1], color="black", lw=size*0.15, solid_capstyle="round", transform=trans, zorder=1)
    ax.plot([0.7, 0.3], [0.1, 0.1], color="black", lw=size*0.15, solid_capstyle="round", transform=trans, zorder=1)
    # Straw
    for dx in [-0.8, -0.75, -0.7]: ax.plot([dx, dx-0.1], [0.1, 0.0], color="black", lw=size*0.04, transform=trans, zorder=0)
    for dx in [0.8, 0.75, 0.7]: ax.plot([dx, dx+0.1], [0.1, 0.0], color="black", lw=size*0.04, transform=trans, zorder=0)
    # Scarf
    ax.fill([-0.2, 0.2, 0], [0.15, 0.15, -0.1], color="white", edgecolor="black", lw=size*0.04, transform=trans, zorder=4)
    # Head
    ax.add_patch(patches.FancyBboxPatch((-0.2, 0.2), 0.4, 0.4, boxstyle="round,pad=0.05", facecolor="black", edgecolor="none", transform=trans, zorder=5))
    # Hat
    ax.fill([-0.5, 0.5, 0.4, -0.4], [0.6, 0.6, 0.7, 0.7], color="black", edgecolor="none", transform=trans, zorder=6)
    ax.fill([-0.3, 0.3, 0.2, -0.1], [0.65, 0.65, 1.0, 0.95], color="black", edgecolor="none", transform=trans, zorder=6)
    ax.fill([-0.1, 0.1, 0.05, -0.15], [0.75, 0.7, 0.85, 0.9], color="white", edgecolor="none", transform=trans, zorder=7)
    # Face
    ax.add_patch(patches.Circle((-0.1, 0.45), 0.04, color="white", transform=trans, zorder=7))
    ax.add_patch(patches.Circle((0.1, 0.45), 0.04, color="white", transform=trans, zorder=7))
    mx = np.linspace(-0.15, 0.15, 5)
    my = 0.3 + 0.02 * np.array([1, -1, 1, -1, 1])
    ax.plot(mx, my, color="white", lw=size*0.02, transform=trans, zorder=7)

def draw_sunflower_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    t = np.linspace(0, 2*np.pi, 200)
    r_petals = 0.8 + 0.2 * np.abs(np.sin(16 * t/2))**1.5
    ax.fill(r_petals * np.cos(t), r_petals * np.sin(t), color="black", edgecolor="none", transform=trans, zorder=2)
    for a in np.linspace(0, 2*np.pi, 16, endpoint=False):
        ax.plot([0.3*np.cos(a), 0.95*np.cos(a)], [0.3*np.sin(a), 0.95*np.sin(a)], color="white", lw=size*0.04, transform=trans, zorder=3)
    ax.add_patch(patches.Circle((0,0), 0.45, facecolor="black", edgecolor="white", lw=size*0.08, transform=trans, zorder=4))
    for v in np.linspace(-0.35, 0.35, 5):
        ax.plot([v, v], [-0.3, 0.3], color="white", lw=size*0.02, transform=trans, zorder=5)
        ax.plot([-0.3, 0.3], [v, v], color="white", lw=size*0.02, transform=trans, zorder=5)

def draw_corncob_detailed(ax, cx, cy, size, angle):
    rad = np.deg2rad(angle)
    trans = transforms.Affine2D().scale(size).rotate(rad).translate(cx, cy) + ax.transData
    t = np.linspace(0, 2*np.pi, 60)
    ax.fill(0.25 * np.cos(t), 0.6 * np.sin(t), color="black", edgecolor="none", transform=trans, zorder=2)
    for lx in np.linspace(-0.15, 0.15, 3):
        ax.plot([lx, lx], [-0.5, 0.5], color="white", lw=size*0.03, transform=trans, zorder=3)
    for ly in np.linspace(-0.4, 0.4, 6):
        ax.plot([-0.2, 0.2], [ly, ly], color="white", lw=size*0.03, transform=trans, zorder=3)
    ax.fill([-0.1, -0.4, -0.5, -0.1], [-0.4, -0.1, -0.4, -0.6], color="black", edgecolor="none", transform=trans, zorder=1)
    ax.plot([-0.1, -0.4], [-0.4, -0.3], color="white", lw=size*0.04, transform=trans, zorder=3)
    ax.fill([0.1, 0.4, 0.5, 0.1], [-0.4, -0.1, -0.4, -0.6], color="black", edgecolor="none", transform=trans, zorder=1)
    ax.plot([0.1, 0.4], [-0.4, -0.3], color="white", lw=size*0.04, transform=trans, zorder=3)

def main():
    fig, ax = setup_ax()
    cols = 8; rows = 12
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    for i in range(-2, cols+3):
        for j in range(-2, rows+3):
            cx = i * spacing_x; cy = j * spacing_y
            if j % 2 != 0: cx += spacing_x / 2
            obj_idx = j % 3
            if obj_idx == 0: draw_scarecrow_detailed(ax, cx, cy, size=3.8)
            elif obj_idx == 1: draw_corncob_detailed(ax, cx, cy, size=4.5, angle=45)
            else: draw_sunflower_detailed(ax, cx, cy, size=3.8)
    save(fig, "abstract autumn scarecrow sunflower corncob glyph solid alternating row grid pattern black white texture")

if __name__ == "__main__":
    main()
