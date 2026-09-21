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


def abstract_parallel_lines_nested_rectangle_tunnel_perspective_pattern_black_white_texture():
    """Persegi bersarang dengan pergeseran pusat bertahap menciptakan efek lorong perspektif 3D"""
    fig, ax = setup_ax()

    n_rects = 38
    # Titik lenyap perspektif (vanishing point) di posisi asimetris
    target_cx, target_cy = 28.0, 72.0
    outer_cx, outer_cy = 50.0, 50.0

    for i in range(n_rects):
        t = i / (n_rects - 1)  # 0 (paling luar) sampai 1 (paling dalam)
        # Interpolasi pusat
        cx = (1 - t) * outer_cx + t * target_cx
        cy = (1 - t) * outer_cy + t * target_cy

        # Ukuran setengah sisi persegi
        half_w = 54.0 * (1 - t * 0.94)
        half_h = 54.0 * (1 - t * 0.94)

        # Ketebalan garis bertambah ke arah luar
        lw = 1.0 + 2.6 * ((1 - t) ** 1.2)

        rect = plt.Rectangle(
            (cx - half_w, cy - half_h),
            half_w * 2,
            half_h * 2,
            fill=False,
            edgecolor="black",
            linewidth=lw,
            joinstyle="miter",
        )
        ax.add_patch(rect)

    save(fig, "abstract parallel lines nested rectangle tunnel perspective pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_nested_rectangle_tunnel_perspective_pattern_black_white_texture()
