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


def abstract_parallel_lines_asymmetric_density_circle_offcenter_pattern_black_white_texture():
    """Garis paralel dengan modulasi densitas lingkaran di posisi asimetris golden ratio"""
    fig, ax = setup_ax()

    # Titik pusat densitas di kuadran asimetris (golden focal point)
    cx, cy = 68.0, 32.0
    radius_scale = 36.0

    n_lines = 68
    y_vals = np.linspace(-5, 105, n_lines)

    for y in y_vals:
        # Segmentasi sepanjang garis horizontal untuk membentuk gradasi densitas 2D
        n_pts = 200
        x_pts = np.linspace(-5, 105, n_pts)
        dx = x_pts[1] - x_pts[0]

        # Hitung jarak tiap titik ke (cx, cy)
        dist = np.hypot(x_pts - cx, y - cy)
        density = np.exp(-((dist / radius_scale) ** 2) * 2.2)

        # Plot garis dengan segmentasi segmen tebal-tipis berkesinambungan
        for j in range(n_pts - 1):
            d_val = (density[j] + density[j + 1]) / 2.0
            lw = 0.6 + 3.8 * d_val
            ax.plot([x_pts[j], x_pts[j + 1]], [y, y], color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines asymmetric density circle offcenter pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_asymmetric_density_circle_offcenter_pattern_black_white_texture()
