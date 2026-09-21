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


def abstract_parallel_lines_lissajous_warp_mesh_pattern_black_white_texture():
    """Wild: grid of lines where each axis is independently warped by a Lissajous function"""
    fig, ax = setup_ax()

    # Lissajous warp: x' = x + A*sin(b*y/100 * 2pi + phi_x)
    #                 y' = y + C*sin(d*x/100 * 2pi + phi_y)
    A = 8.0   # horizontal warp amplitude
    b = 3     # Lissajous freq for horizontal lines (vertical modulation)
    C = 8.0   # vertical warp amplitude
    d = 4     # Lissajous freq for vertical lines (horizontal modulation)
    phi_x = np.pi / 4
    phi_y = np.pi / 6

    t = np.linspace(0, 100, 500)

    # Horizontal lines
    n_h = 48
    for i in range(n_h):
        y0 = i * 100 / (n_h - 1)
        x_pts = t
        y_pts = y0 + A * np.sin(b * t / 100 * 2 * np.pi + phi_x)
        lw = 0.6 + 0.4 * abs(np.sin(np.pi * i / n_h))
        ax.plot(x_pts, y_pts, color="black", linewidth=lw, solid_capstyle="round")

    # Vertical lines
    n_v = 48
    for j in range(n_v):
        x0 = j * 100 / (n_v - 1)
        x_pts = x0 + C * np.sin(d * t / 100 * 2 * np.pi + phi_y)
        y_pts = t
        lw = 0.6 + 0.4 * abs(np.sin(np.pi * j / n_v))
        ax.plot(x_pts, y_pts, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines lissajous warp mesh pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_lissajous_warp_mesh_pattern_black_white_texture()
