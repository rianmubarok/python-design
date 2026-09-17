import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


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


def abstract_grid_tessellation_hexagonal_truchet_tile_pattern_black_white_texture():
    """Hexagonal Truchet tiling.

    Each pointy-top hexagonal tile connects three alternating edge midpoints with
    arcs whose centres sit on the tile corners and whose radius is half an edge.
    The arcs therefore meet the neighbouring tiles exactly on the shared edge
    midpoints, producing one continuous space-filling curve.
    """
    fig, ax = setup_ax()

    r = 6.0
    dx = r * np.sqrt(3)
    dy = r * 1.5

    n = 7
    for row in range(-n, n + 1):
        for col in range(-n, n + 1):
            cx = 50 + col * dx
            if row % 2 != 0:
                cx += dx / 2
            cy = 50 + row * dy

            # Two alternating corner sets -> the two Truchet rotation states.
            base = 30.0 if np.random.choice([0, 1]) == 0 else 90.0
            for k in range(3):
                a = base + 120.0 * k
                corner_x = cx + r * np.cos(np.radians(a))
                corner_y = cy + r * np.sin(np.radians(a))
                arc = Arc(
                    (corner_x, corner_y),
                    r,
                    r,
                    angle=0,
                    theta1=a + 120.0,
                    theta2=a + 240.0,
                    color="black",
                    linewidth=1.5,
                )
                ax.add_patch(arc)

    save(fig, "abstract grid tessellation hexagonal truchet tile pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_hexagonal_truchet_tile_pattern_black_white_texture()
