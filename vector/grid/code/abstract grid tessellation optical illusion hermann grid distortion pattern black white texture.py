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
    Optical Illusion Hermann Grid Distortion.

    The classic Hermann Grid (black squares separated by thin white gutters,
    which makes faint grey spots appear at the intersections) is warped by a
    smooth radial "spherical lens" mapping. Every corner of every square is
    displaced individually through the same monotonic function, so:
      * adjacent squares share the exact same distorted edge -> the white
        gutters stay open and uniform (the illusion is preserved), and
      * the lattice curves organically instead of the squares being merely
        scaled in place (which made them overlap and close the gutters).
    """
    fig, ax = setup_ax()

    import matplotlib.patches as patches

    grid_size = 40
    span = 120.0                      # base grid spans -10 .. 110
    cell_w = span / grid_size
    gap = cell_w * 0.22               # white gutter between squares

    strength = 0.85                   # peak magnification at the centre
    sigma = 30.0                      # reach of the lens effect

    def lens(x, y):
        """Monotonic radial (barrel/spherical) mapping centred on (50, 50)."""
        dx, dy = x - 50.0, y - 50.0
        r = np.hypot(dx, dy)
        scale = 1.0 + strength * np.exp(-(r / sigma) ** 2)   # >1 centre, ~1 edge
        return 50.0 + dx * scale, 50.0 + dy * scale, scale

    for row in range(grid_size):
        for col in range(grid_size):
            x_min = -10 + col * cell_w + gap / 2
            y_min = -10 + row * cell_w + gap / 2
            x_max = x_min + (cell_w - gap)
            y_max = y_min + (cell_w - gap)

            # Distort all four corners individually so the squares curve smoothly
            p1x, p1y, _ = lens(x_min, y_min)   # bottom-left
            p2x, p2y, _ = lens(x_max, y_min)   # bottom-right
            p3x, p3y, _ = lens(x_max, y_max)   # top-right
            p4x, p4y, _ = lens(x_min, y_max)   # top-left

            ax.add_patch(patches.Polygon(
                [(p1x, p1y), (p2x, p2y), (p3x, p3y), (p4x, p4y)],
                closed=True, facecolor="black", edgecolor="none"))

            # Adaptive white accent dot at the distorted square centre
            ccx, ccy, sc = lens((x_min + x_max) / 2, (y_min + y_max) / 2)
            if 2.0 < ccx < 98.0 and 2.0 < ccy < 98.0:
                ax.add_patch(patches.Circle(
                    (ccx, ccy), (cell_w - gap) * 0.05 * sc,
                    facecolor="white", edgecolor="none"))

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    save(fig, "abstract grid tessellation optical illusion hermann grid distortion pattern black white texture")


if __name__ == "__main__":
    draw()
