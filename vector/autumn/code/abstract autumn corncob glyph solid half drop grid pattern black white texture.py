import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
from pathlib import Path as FilePath
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")
SCRIPT_DIR = FilePath(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax

def save(fig, name):
    fig.savefig(JPG_DIR/f"{name} {DATE}.jpg", dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(SVG_DIR/f"{name} {DATE}.svg", format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Saved: {name}")

def draw_corncob(ax, cx, cy, size, angle=0):
    trans = transforms.Affine2D().scale(size).rotate_deg(angle).translate(cx, cy) + ax.transData

    # === BODY: tapered oval (wider middle, pointed top & bottom) ===
    t = np.linspace(0, 2*np.pi, 120)
    # Use superellipse-like shape: taper top & bottom
    bx = 0.28 * np.cos(t) * (1 - 0.18 * np.cos(t)**2)
    by = 0.68 * np.sin(t)
    # Center
    cx_off = (np.max(bx) + np.min(bx)) / 2
    cy_off = (np.max(by) + np.min(by)) / 2
    bx = bx - cx_off
    by = by - cy_off
    ax.fill(bx, by, color="black", edgecolor="none", transform=trans, zorder=2)

    # === KERNEL GRID: horizontal rows + vertical column dividers ===
    n_rows = 9
    n_cols = 4
    for ri in range(1, n_rows):
        ry = -0.58 + ri * (1.16 / n_rows)
        # Width of corn at this y (ellipse width)
        half_w = 0.27 * np.sqrt(max(0, 1 - (ry / 0.68)**2)) * 0.92
        ax.plot([-half_w, half_w], [ry, ry], color="white", lw=size*0.028, solid_capstyle="round", transform=trans, zorder=3)

    for ci in range(1, n_cols):
        col_x = -0.21 + ci * (0.42 / n_cols)
        ax.plot([col_x, col_x], [-0.55, 0.55], color="white", lw=size*0.028, solid_capstyle="round", transform=trans, zorder=3)

    # === TASSEL (silk threads at top) ===
    tassel_base_y = 0.65
    for tx in np.linspace(-0.12, 0.12, 6):
        # Each strand curves outward slightly
        strand_y = np.linspace(tassel_base_y, tassel_base_y + 0.28, 20)
        strand_x = np.linspace(tx, tx + tx * 0.4, 20)
        ax.plot(strand_x, strand_y, color="black", lw=size*0.025, solid_capstyle="round", transform=trans, zorder=4)

    # === HUSK LEAVES (2 peeling leaves at bottom) ===
    # Left husk
    lhx = [-0.05, -0.35, -0.45, -0.22, -0.05]
    lhy = [-0.25,  0.05, -0.35, -0.68, -0.55]
    cx_lh = (np.max(lhx) + np.min(lhx)) / 2
    cy_lh = (np.max(lhy) + np.min(lhy)) / 2
    ax.fill([x - cx_lh + 0 for x in lhx],
            [y - cy_lh + -0.05 for y in lhy],
            color="black", edgecolor="none", transform=trans, zorder=1)
    ax.plot([-0.05, -0.35], [-0.30, 0.00], color="white", lw=size*0.03, transform=trans, zorder=3)

    # Right husk
    rhx = [0.05, 0.35, 0.45, 0.22, 0.05]
    rhy = [-0.25, 0.05, -0.35, -0.68, -0.55]
    ax.fill([x - (np.max(rhx)+np.min(rhx))/2 + 0 for x in rhx],
            [y - (np.max(rhy)+np.min(rhy))/2 + -0.05 for y in rhy],
            color="black", edgecolor="none", transform=trans, zorder=1)
    ax.plot([0.05, 0.35], [-0.30, 0.00], color="white", lw=size*0.03, transform=trans, zorder=3)

    # === STEM nub at bottom ===
    ax.plot([0, 0], [-0.68, -0.80], color="black", lw=size*0.07,
            solid_capstyle="round", transform=trans, zorder=2)

def main():
    fig, ax = setup_ax()

    # Half-drop grid: single corncob per cell, alternate cols drop by half
    cols = 5
    rows = 6
    spacing_x = 100 / cols
    spacing_y = 100 / rows

    # Alternate angle: upright and slightly tilted for rhythm
    angles = [0, -10, 0, 10]

    for i in range(-1, cols + 2):
        for j in range(-2, rows + 3):
            cx = i * spacing_x
            # Half-drop: odd columns shift down by half
            cy = j * spacing_y + (spacing_y * 0.5 if i % 2 == 1 else 0)
            angle = angles[(i + j * 2) % len(angles)]
            draw_corncob(ax, cx, cy, size=7.5, angle=angle)

    save(fig, "abstract autumn corncob glyph solid half drop grid pattern black white texture")

if __name__ == "__main__":
    main()
