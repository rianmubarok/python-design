import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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
    """Rhombille tumbling blocks grid tessellation with seamless wave deformation."""
    fig, ax = setup_ax()

    scale = 5.5
    dx = scale * np.sqrt(3)
    dy = scale * 1.5

    cols, rows = 18, 18
    center_x = (cols - 1) * (dx / 2.0) / 2.0
    center_y = (rows - 1) * dy / 2.0

    # Transformation wave function for continuous deformation without gaps
    def warp(x, y):
        w = 0.8 * np.sin(x * 0.08) + 0.6 * np.cos(y * 0.1)
        return x, y + w

    for row in range(rows):
        for col in range(cols):
            cx = col * (dx / 2.0)
            cy = row * dy + (dy / 3.0 if col % 2 else 0)

            # Center point
            pcx, pcy = warp(cx, cy)

            # 3D Cube Vertices in Isometric projection
            v0 = warp(cx, cy + scale)  # Top
            v1 = warp(cx + scale * np.sqrt(3) / 2, cy + scale / 2)  # Top Right
            v2 = warp(cx + scale * np.sqrt(3) / 2, cy - scale / 2)  # Bottom Right
            v3 = warp(cx, cy - scale)  # Bottom
            v4 = warp(cx - scale * np.sqrt(3) / 2, cy - scale / 2)  # Bottom Left
            v5 = warp(cx - scale * np.sqrt(3) / 2, cy + scale / 2)  # Top Left

            # 3 Rhombus Faces
            f_top = [[pcx, pcy], v1, v0, v5]
            f_right = [[pcx, pcy], v2, v3, v1]
            f_left = [[pcx, pcy], v4, v3, v5]

            # Face 1: Top (White)
            ax.add_patch(
                Polygon(
                    f_top,
                    closed=True,
                    facecolor="white",
                    edgecolor="black",
                    linewidth=0.9,
                    zorder=2,
                )
            )

            # Face 2: Right (Hatched with White Background)
            ax.add_patch(
                Polygon(
                    f_right,
                    closed=True,
                    facecolor="white",
                    edgecolor="black",
                    linewidth=0.9,
                    hatch="////",
                    zorder=2,
                )
            )

            # Face 3: Left (Black Solid)
            ax.add_patch(
                Polygon(
                    f_left,
                    closed=True,
                    facecolor="black",
                    edgecolor="black",
                    linewidth=0.9,
                    zorder=2,
                )
            )

    # Center crop view
    pad = 34.0
    ax.set_xlim(center_x - pad, center_x + pad)
    ax.set_ylim(center_y - pad, center_y + pad)

    save(
        fig,
        "abstract grid tessellation rhombille tumbling rounded vertex pattern black white texture",
    )


if __name__ == "__main__":
    draw()