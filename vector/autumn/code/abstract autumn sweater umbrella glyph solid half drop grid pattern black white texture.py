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

def draw_sweater_detailed(ax, cx, cy, size):
    trans = transforms.Affine2D().scale(size).translate(cx, cy) + ax.transData
    torso_x = [-0.4, 0.4, 0.35, -0.35]; torso_y = [0.4, 0.4, -0.6, -0.6]
    ax.fill(torso_x, torso_y, color="black", edgecolor="none", transform=trans, zorder=2)
    sl_x = [-0.4, -0.85, -0.75, -0.35]; sl_y = [0.4, -0.2, -0.3, 0.0]
    ax.fill(sl_x, sl_y, color="black", edgecolor="none", transform=trans, zorder=1)
    sr_x = [0.4, 0.85, 0.75, 0.35]; sr_y = [0.4, -0.2, -0.3, 0.0]
    ax.fill(sr_x, sr_y, color="black", edgecolor="none", transform=trans, zorder=1)
    ax.fill([-0.25, 0.25, 0.2, -0.2], [0.35, 0.35, 0.65, 0.65], color="black", edgecolor="none", transform=trans, zorder=3)
    for cx_line in np.linspace(-0.15, 0.15, 5): ax.plot([cx_line, cx_line], [0.4, 0.6], color="white", lw=size*0.03, solid_capstyle="round", transform=trans, zorder=4)
    ax.plot([-0.35, 0.35], [-0.45, -0.45], color="white", lw=size*0.03, transform=trans, zorder=4)
    for cx_line in np.linspace(-0.25, 0.25, 8): ax.plot([cx_line, cx_line], [-0.55, -0.45], color="white", lw=size*0.03, solid_capstyle="round", transform=trans, zorder=4)
    ax.plot([-0.77, -0.68], [-0.15, -0.25], color="white", lw=size*0.04, transform=trans, zorder=4)
    ax.plot([0.77, 0.68], [-0.15, -0.25], color="white", lw=size*0.04, transform=trans, zorder=4)
    kt = np.linspace(0, 5*np.pi, 60)
    kx1 = 0.08 * np.sin(kt); ky1 = 0.35 - 0.75 * (kt / (5*np.pi))
    ax.plot(kx1, ky1, color="white", lw=size*0.04, transform=trans, zorder=4)
    ax.plot(-0.08 * np.sin(kt), ky1, color="white", lw=size*0.04, transform=trans, zorder=4)
    for y_v in np.linspace(-0.3, 0.2, 5):
        ax.plot([-0.25, -0.2, -0.15], [y_v+0.05, y_v, y_v+0.05], color="white", lw=size*0.03, solid_capstyle="round", transform=trans, zorder=4)
        ax.plot([0.15, 0.2, 0.25], [y_v+0.05, y_v, y_v+0.05], color="white", lw=size*0.03, solid_capstyle="round", transform=trans, zorder=4)

def draw_umbrella_detailed(ax, cx, cy, size, angle):
    rad = np.deg2rad(angle)
    trans = transforms.Affine2D().scale(size).rotate(rad).translate(cx, cy) + ax.transData
    t = np.linspace(0, np.pi, 100)
    cx_top = 0.8 * np.cos(t); cy_top = 0.8 * np.sin(t)
    st = np.linspace(-0.8, 0.8, 100)
    cy_bottom = 0.15 * np.abs(np.sin(st * np.pi / 0.4))
    x_poly = np.concatenate([cx_top, st[::-1]])
    y_poly = np.concatenate([cy_top, cy_bottom[::-1]])
    y_cent = y_poly - 0.4
    ax.fill(x_poly, y_cent, color="black", edgecolor="none", transform=trans, zorder=2)
    ax.plot([-0.4, 0.0], [0.15-0.4, 0.8-0.4], color="white", lw=size*0.06, transform=trans, zorder=3)
    ax.plot([0.4, 0.0], [0.15-0.4, 0.8-0.4], color="white", lw=size*0.06, transform=trans, zorder=3)
    ax.plot([0, 0], [0.0-0.4, -0.65-0.4], color="black", lw=size*0.08, transform=trans, zorder=1)
    t_hook = np.linspace(np.pi, 2*np.pi, 20)
    ax.plot(0.15 + 0.15*np.cos(t_hook), -0.65-0.4 + 0.15*np.sin(t_hook), color="black", lw=size*0.08, transform=trans, zorder=1)
    ax.plot([0, 0], [0.8-0.4, 0.95-0.4], color="black", lw=size*0.08, transform=trans, zorder=1)

def main():
    fig, ax = setup_ax()
    cols = 8; rows = 8
    spacing_x = 100 / cols
    spacing_y = 100 / rows
    for i in range(-2, cols+3):
        for j in range(-2, rows+3):
            cx = i * spacing_x; cy = j * spacing_y
            if j % 2 != 0: cx += spacing_x / 2
            if (i + j) % 2 == 0:
                draw_sweater_detailed(ax, cx, cy, size=4.0)
            else:
                draw_umbrella_detailed(ax, cx, cy, size=4.0, angle=15)
    save(fig, "abstract autumn sweater umbrella glyph solid half drop grid pattern black white texture")

if __name__ == "__main__":
    main()
