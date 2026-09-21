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
    3D Wireframe Terrain Topography.

    The terrain is rendered back-to-front with each mesh cell filled as an
    opaque white polygon. Because nearer cells are painted last, they mask the
    lines of the geometry behind them (painter's algorithm), giving a solid
    hidden-surface look instead of every line bleeding through every other one.
    """
    fig, ax = setup_ax()
    rng = np.random.default_rng(42)

    n_lines = 45
    # Grid in 3D space (overflows the canvas so there are no barren borders)
    x = np.linspace(-40.0, 140.0, n_lines)
    z = np.linspace(15.0, 160.0, n_lines)
    X, Z = np.meshgrid(x, z)

    # Balanced, organic pseudo-noise terrain heights (Y)
    Y = np.zeros_like(X)
    for f in [0.03, 0.07, 0.14]:
        phase_x = rng.uniform(0, 2 * np.pi)
        phase_z = rng.uniform(0, 2 * np.pi)
        amp = 1.0 / f
        Y += np.sin(X * f + phase_x) * np.cos(Z * f + phase_z) * amp * 0.35

    # Project 3D (X, Y, Z) to 2D screen coordinates with a simple perspective
    cam_z = -60
    fov = 130.0
    depth = Z - cam_z

    screen_x = 50.0 + (X - 50.0) * fov / depth
    screen_y = -24.0 + Y * (fov / depth) + depth * 0.55

    import matplotlib.patches as patches

    # Painter's algorithm: farthest rows first so nearer cells occlude them
    for i in reversed(range(n_lines - 1)):
        for j in range(n_lines - 1):
            p1 = [screen_x[i, j], screen_y[i, j]]          # bottom-left
            p2 = [screen_x[i, j + 1], screen_y[i, j + 1]]  # bottom-right
            p3 = [screen_x[i + 1, j + 1], screen_y[i + 1, j + 1]]  # top-right
            p4 = [screen_x[i + 1, j], screen_y[i + 1, j]]  # top-left

            poly = patches.Polygon([p1, p2, p3, p4], closed=True,
                                   facecolor="white", edgecolor="black", linewidth=0.8)
            ax.add_patch(poly)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    save(fig, "abstract grid tessellation 3d wireframe terrain topography pattern black white texture")


if __name__ == "__main__":
    draw()
