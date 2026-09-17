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
    Isometric Impossible Stairs / Escher blocks.

    Every tile is a mathematically exact isometric cube: the hexagonal
    silhouette is split into three clean rhombi (top / left / right), so the
    120-degree angles meet at the centre. The honeycomb lattice uses the
    correct 30-degree spacing (columns 2*w apart, alternate rows offset by w),
    which makes neighbouring cubes interlock edge-to-edge instead of overlapping.
    A deterministic terracing height field turns it into an Escher-like
    staircase texture.
    """
    import matplotlib.patches as patches

    fig, ax = setup_ax()

    cube_size = 3.5
    angle = np.pi / 6  # 30 degrees
    h = cube_size * np.sin(angle)   # half height of the hexagon
    w = cube_size * np.cos(angle)   # half width of the hexagon

    # Exact isometric vertices (regular hexagon) centred on (0, 0)
    p1 = np.array([0.0, cube_size])   # top vertex
    p2 = np.array([w, h])             # upper right vertex
    p3 = np.array([w, -h])            # lower right vertex
    p4 = np.array([0.0, -cube_size])  # bottom vertex
    p5 = np.array([-w, -h])           # lower left vertex
    p6 = np.array([-w, h])            # upper left vertex
    center = np.array([0.0, 0.0])     # middle intersection

    # The three visible cube faces, defined as clean rhombi
    face_top = [center, p2, p1, p6, center]
    face_left = [center, p6, p5, p4, center]
    face_right = [center, p4, p3, p2, center]

    n = 24
    z_step = cube_size - h

    # Deterministic smooth height field -> terraced plateaus / stairs
    heights = np.zeros((n, n))
    for r in range(n):
        for c in range(n):
            heights[r, c] = int((np.sin(r * 0.4) + np.cos(c * 0.4)) * 2.5)

    # Honeycomb lattice: columns are 2*w apart, every other row is offset by w,
    # rows are (cube_size + h) apart. Render back-to-front (top rows first) so
    # foreground blocks always occlude the background correctly.
    for row in reversed(range(n)):
        for col in range(n):
            cx = col * 2 * w + (row % 2) * w
            cy = row * (cube_size + h) + heights[row, col] * z_step

            # Left face: solid black fill
            ax.add_patch(patches.Polygon(
                np.array(face_left) + [cx, cy], closed=True,
                facecolor="black", edgecolor="black", linewidth=1.2))
            # Right face: structured line hatching
            ax.add_patch(patches.Polygon(
                np.array(face_right) + [cx, cy], closed=True,
                facecolor="white", edgecolor="black", linewidth=1.2, hatch="\\\\\\\\"))
            # Top face: drawn last so it covers the side boundaries cleanly
            ax.add_patch(patches.Polygon(
                np.array(face_top) + [cx, cy], closed=True,
                facecolor="white", edgecolor="black", linewidth=1.2))

    # Square, centred composition that fills the canvas cleanly
    x0, x1 = ax.dataLim.intervalx
    y0, y1 = ax.dataLim.intervaly
    ccx = (x0 + x1) / 2
    ccy = (y0 + y1) / 2
    half = max(x1 - x0, y1 - y0) / 2 * 1.03
    ax.set_xlim(ccx - half, ccx + half)
    ax.set_ylim(ccy - half, ccy + half)

    save(fig, "abstract grid tessellation isometric impossible stairs pattern black white texture")


if __name__ == "__main__":
    draw()
