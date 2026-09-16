import numpy as np
import matplotlib.pyplot as plt
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


def draw_parallel_group(ax, x_start, x_end, y_centre, height, n_lines, lw, depth):
    """Draw a group of horizontal parallel lines within a bounding band."""
    y_positions = np.linspace(y_centre - height / 2, y_centre + height / 2, n_lines)
    alpha = 0.4 + 0.6 * (1 - depth / 4.0)
    for y in y_positions:
        if -6 < y < 106:
            ax.plot([max(x_start, -5), min(x_end, 105)], [y, y],
                    color="black", linewidth=lw, solid_capstyle="round",
                    alpha=alpha)


def abstract_parallel_lines_fractal_recursive_subdivision_pattern_black_white_texture():
    """
    Wild: Fractal recursive parallel lines. Start with 4 horizontal bands.
    Each band subdivides into 3 smaller parallel sub-bands, offset slightly.
    4 recursion levels create a self-similar hierarchical tree of parallel lines.
    """
    fig, ax = setup_ax()

    def recurse(x_start, x_end, y_centre, height, depth, max_depth):
        if depth >= max_depth:
            return

        # Number of lines per group depends on depth
        n_lines = max(2, 6 - depth)
        lw = max(0.2, 1.4 - depth * 0.3)

        # Draw the parallel lines for this level
        draw_parallel_group(ax, x_start, x_end, y_centre, height, n_lines, lw, depth)

        # Subdivide into 3 sub-bands
        # Each sub-band is 1/3.5 of the height, distributed evenly
        sub_height = height / 3.8
        # Offset: narrow the x-span slightly each level for visual depth
        x_margin = (x_end - x_start) * 0.02
        sub_x_start = x_start + x_margin
        sub_x_end = x_end - x_margin

        offsets = [-height / 3.2, 0, height / 3.2]
        for off in offsets:
            sub_y = y_centre + off
            recurse(sub_x_start, sub_x_end, sub_y, sub_height, depth + 1, max_depth)

    # Initial 4 bands spanning the canvas
    initial_bands = 4
    band_height = 100.0 / initial_bands
    max_depth = 4

    for i in range(initial_bands):
        y_c = (i + 0.5) * band_height
        recurse(-5, 105, y_c, band_height * 0.85, 0, max_depth)

    save(fig, "abstract parallel lines fractal recursive subdivision pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_fractal_recursive_subdivision_pattern_black_white_texture()
