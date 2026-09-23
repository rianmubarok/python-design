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

def draw_pie_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    px = [0, 0.6, -0.6, 0]; py = [-0.6, 0.4, 0.4, -0.6]
    ax.fill(px, py, color="black", edgecolor="none", transform=trans, zorder=2)
    crust_t = np.linspace(-0.65, 0.65, 50)
    crust_y = 0.4 + 0.1 * np.abs(np.sin(crust_t * 5 * np.pi / 0.65))
    ax.fill(np.concatenate([crust_t, crust_t[::-1]]), np.concatenate([crust_y, np.full_like(crust_t, 0.3)]), color="black", edgecolor="none", transform=trans, zorder=3)
    ax.plot([0, 0.3], [0, 0.3], color="white", lw=size*0.06, transform=trans, zorder=4)
    ax.plot([0, -0.3], [0, 0.3], color="white", lw=size*0.06, transform=trans, zorder=4)
    ax.plot([-0.2, 0.2], [0.1, 0.1], color="white", lw=size*0.06, transform=trans, zorder=4)
    st = np.linspace(0, 1, 20)
    ax.plot(-0.2 + 0.05*np.sin(st*10), 0.5 + 0.3*st, color="black", lw=size*0.06, transform=trans, zorder=1)
    ax.plot(0.2 + 0.05*np.sin(st*10 + 2), 0.5 + 0.3*st, color="black", lw=size*0.06, transform=trans, zorder=1)

def draw_pomegranate_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    t = np.linspace(0, 2*np.pi, 80)
    x = 0.7 * np.cos(t); y = 0.65 * np.sin(t) - 0.05*np.cos(2*t)
    y_cent = y - (np.max(y) + np.min(y))/2
    crown_x = [-0.15, -0.2, -0.05, 0, 0.05, 0.2, 0.15]; crown_y = [0.6, 0.85, 0.7, 0.9, 0.7, 0.85, 0.6]
    crown_y_cent = np.array(crown_y) - (np.max(y) + np.min(y))/2
    ax.fill(x, y_cent, color="black", edgecolor="none", transform=trans, zorder=2)
    ax.fill(crown_x, crown_y_cent, color="black", edgecolor="none", transform=trans, zorder=2)
    cx_cut = 0.2 + 0.2*np.cos(t); cy_cut = 0.2*np.sin(t) - (np.max(y) + np.min(y))/2
    ax.fill(cx_cut, cy_cut, color="white", edgecolor="none", transform=trans, zorder=3)
    for sx, sy in [(0.15, 0.05), (0.25, 0.1), (0.18, -0.1), (0.28, -0.05), (0.3, 0.05)]:
        ax.add_patch(patches.Circle((sx, sy - (np.max(y) + np.min(y))/2), 0.04, color="black", transform=trans, zorder=4))
    ax.plot([-0.5, -0.2], [-0.3, -0.5], color="white", lw=size*0.06, transform=trans, zorder=3)

def draw_chestnut_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    t = np.linspace(0, 2*np.pi, 80)
    x = 0.5 * np.cos(t); y = 0.4 * np.sin(t)
    y = np.where(y < -0.1, -0.1, y)
    y += 0.3 * np.abs(np.sin(t/2))**3 * (1 if np.mean(np.sin(t)) > 0 else -1)
    y_offset = (np.max(y) + np.min(y))/2
    y -= y_offset
    ax.fill(x, y, color="black", edgecolor="none", transform=trans, zorder=2)
    st = np.linspace(np.pi*0.8, np.pi*2.2, 30)
    sx = 0.6 * np.cos(st); sy = 0.2 * np.sin(st) - 0.15 - y_offset
    sy += 0.1 * np.cos(20*st)
    ax.fill(np.concatenate([[0], sx, [0]]), np.concatenate([[0], sy, [0]]), color="black", edgecolor="none", transform=trans, zorder=1)
    ax.plot([0.1, 0.3], [0.1-y_offset, 0.2-y_offset], color="white", lw=size*0.1, transform=trans, zorder=3)
    ax.plot([0.15, 0.25], [0.05-y_offset, 0.12-y_offset], color="white", lw=size*0.06, transform=trans, zorder=3)

def main():
    fig, ax = setup_ax()
    cols = 9; rows = 12
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    for i in range(-2, cols+3):
        for j in range(-2, rows+3):
            cx = i * spacing_x; cy = j * spacing_y
            if j % 2 != 0: cx += spacing_x / 2
            obj_idx = j % 3
            if obj_idx == 0: draw_pie_detailed(ax, cx, cy, size=4.0)
            elif obj_idx == 1: draw_pomegranate_detailed(ax, cx, cy, size=4.0)
            else: draw_chestnut_detailed(ax, cx, cy, size=4.0)
    save(fig, "abstract autumn pie pomegranate chestnut glyph solid staggered row grid pattern black white texture")

if __name__ == "__main__":
    main()
