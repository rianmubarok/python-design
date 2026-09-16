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
    Tesseract (4D hypercube) projected into 2D using parallel perspective.
    Multiple nested cubes connected by parallel edges, with additional
    parallel line fills along each face to create the pattern texture.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0

    # Generate multiple nested tesseract-like projections
    n_layers = 12
    for layer in range(n_layers):
        t = layer / (n_layers - 1)
        # Outer cube size
        s_outer = 48 - 38 * t
        # Inner cube size (offset for 4D projection)
        s_inner = s_outer * 0.55
        # Offset of inner cube center from outer
        offset = s_outer * 0.2 * (1 - t * 0.3)

        # Outer square corners
        o_corners = np.array([
            [cx - s_outer, cy - s_outer],
            [cx + s_outer, cy - s_outer],
            [cx + s_outer, cy + s_outer],
            [cx - s_outer, cy + s_outer],
        ])

        # Inner square corners (offset up-right for perspective)
        icx = cx + offset
        icy = cy + offset
        i_corners = np.array([
            [icx - s_inner, icy - s_inner],
            [icx + s_inner, icy - s_inner],
            [icx + s_inner, icy + s_inner],
            [icx - s_inner, icy + s_inner],
        ])

        lw = 0.3 + 0.4 * (1 - t)

        # Draw outer square
        for k in range(4):
            p1 = o_corners[k]
            p2 = o_corners[(k + 1) % 4]
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="black",
                    linewidth=lw, solid_capstyle="round")

        # Draw inner square
        for k in range(4):
            p1 = i_corners[k]
            p2 = i_corners[(k + 1) % 4]
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="black",
                    linewidth=lw, solid_capstyle="round")

        # Connect corresponding corners (the 4D projection edges)
        for k in range(4):
            ax.plot([o_corners[k, 0], i_corners[k, 0]],
                    [o_corners[k, 1], i_corners[k, 1]],
                    color="black", linewidth=lw * 0.7, solid_capstyle="round")

    # Add parallel fill lines across the top face of the outermost cube
    n_fill = 30
    s0 = 48
    offset0 = s0 * 0.2
    for i in range(n_fill):
        t = i / (n_fill - 1)
        # Interpolate between outer top edge and inner top edge
        x1 = cx - s0 + t * (cx + offset0 - s0 * 0.55 - (cx - s0))
        y1 = cy + s0 + t * (cy + offset0 + s0 * 0.55 - (cy + s0))
        x2 = cx + s0 + t * (cx + offset0 + s0 * 0.55 - (cx + s0))
        y2 = y1
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=0.2,
                solid_capstyle="round")

    # Add parallel fill lines across the right face
    for i in range(n_fill):
        t = i / (n_fill - 1)
        x1 = cx + s0 + t * (cx + offset0 + s0 * 0.55 - (cx + s0))
        y1 = cy - s0 + t * (cy + offset0 - s0 * 0.55 - (cy - s0))
        x2 = x1
        y2 = cy + s0 + t * (cy + offset0 + s0 * 0.55 - (cy + s0))
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=0.2,
                solid_capstyle="round")

    save(fig, "abstract parallel lines tesseract hypercube projection pattern black white texture")


if __name__ == "__main__":
    draw()
