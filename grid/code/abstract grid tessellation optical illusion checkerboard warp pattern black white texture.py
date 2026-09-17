import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def draw():
    """
    Optical Illusion Checkerboard Warp.

    A regular checkerboard is warped by a smooth, normalised radial (barrel)
    distortion so the grid flows into a convex 3-D spherical bulge, in the
    spirit of Vasarely's "Vega".

    The displacement is purely radial: X' = cx + DX * factor(R). Because the
    factor is a monotonic function of R, every grid node moves along its own
    ray and adjacent cells keep sharing their corners, so the checkerboard
    stays coherent and no quadrant can collapse or fuse into solid blocks.
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches

    n_cells = 42
    grid_coords = np.linspace(-20.0, 120.0, n_cells + 1)   # overflows the canvas
    X, Y = np.meshgrid(grid_coords, grid_coords)

    cx, cy = 50.0, 50.0
    DX = X - cx
    DY = Y - cy
    R = np.sqrt(DX**2 + DY**2)

    # Smooth spherical bulge profile: magnifies the centre (> 1) and tapers
    # back to 1 at R_max, so the outer frame stays undeformed.
    R_max = 80.0
    Rn = np.minimum(R, R_max) / R_max
    factor = 1.0 + 0.45 * np.cos(Rn * np.pi / 2)

    X_warped = cx + DX * factor
    Y_warped = cy + DY * factor

    for i in range(n_cells):
        for j in range(n_cells):
            if (i + j) % 2 == 0:
                p1 = [X_warped[i, j], Y_warped[i, j]]
                p2 = [X_warped[i, j + 1], Y_warped[i, j + 1]]
                p3 = [X_warped[i + 1, j + 1], Y_warped[i + 1, j + 1]]
                p4 = [X_warped[i + 1, j], Y_warped[i + 1, j]]

                # Edge colour matches the fill to avoid faint white seams
                poly = patches.Polygon([p1, p2, p3, p4], closed=True,
                                       facecolor="black", edgecolor="black", linewidth=0.2)
                ax.add_patch(poly)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    save(fig, "abstract grid tessellation optical illusion checkerboard warp pattern black white texture")


if __name__ == "__main__":
    draw()
