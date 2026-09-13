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


def abstract_parallel_lines_corner_nested_triangle_perspective_pattern_black_white_texture():
    """Segitiga bersarang paralel yang memancar dan membesar ke atas dengan kedalaman perspektif"""
    fig, ax = setup_ax()

    # Titik puncak atas dan dua kaki bawah
    top_apex_base = np.array([50.0, 96.0])
    left_apex_base = np.array([-10.0, 6.0])
    right_apex_base = np.array([110.0, 6.0])
    focal_center = np.array([50.0, 42.0])

    n_triangles = 36

    for i in range(n_triangles):
        t = (i + 1) / n_triangles  # 0 ke 1

        # Interpolasi simpul segitiga dari pusat fokus ke perimeter
        p_top = (1 - t) * focal_center + t * top_apex_base
        p_left = (1 - t) * focal_center + t * left_apex_base
        p_right = (1 - t) * focal_center + t * right_apex_base

        xs = [p_top[0], p_right[0], p_left[0], p_top[0]]
        ys = [p_top[1], p_right[1], p_left[1], p_top[1]]

        lw = 0.8 + 2.8 * (t ** 1.3)
        ax.plot(xs, ys, color="black", linewidth=lw, solid_joinstyle="miter")

    save(fig, "abstract parallel lines corner nested triangle perspective pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_corner_nested_triangle_perspective_pattern_black_white_texture()
