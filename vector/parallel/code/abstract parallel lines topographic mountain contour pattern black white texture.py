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


def abstract_parallel_lines_topographic_mountain_contour_pattern_black_white_texture():
    """Wild: irregular closed contours like a topographic map — mountain eroded by noise"""
    fig, ax = setup_ax()
    cx, cy = 50.0, 50.0
    n_contours = 32
    n_pts = 720

    # Build a "height function" h(angle) for elliptical base + harmonic bumps
    angles = np.linspace(0, 2 * np.pi, n_pts, endpoint=False)
    np.random.seed(SEED)
    # Sum of random harmonics to create terrain ridge
    n_harmonics = 8
    harmonics = np.zeros(n_pts)
    for k in range(1, n_harmonics + 1):
        phase = np.random.uniform(0, 2 * np.pi)
        amp = np.random.uniform(0.3, 1.0) / k
        harmonics += amp * np.cos(k * angles + phase)
    harmonics = (harmonics - harmonics.min()) / (harmonics.max() - harmonics.min())

    # Ellipse base radii
    ra_base, rb_base = 42.0, 36.0

    for level in range(n_contours):
        t = level / (n_contours - 1)  # 0 = outermost, 1 = summit
        # Shrink the ellipse toward centre as level rises
        scale = 1 - t ** 0.85
        ra = ra_base * scale
        rb = rb_base * scale
        # Add terrain roughness that also shrinks toward summit
        roughness = 6.0 * (1 - t) * scale
        r_terrain = roughness * harmonics

        x_pts = cx + (ra + r_terrain) * np.cos(angles)
        y_pts = cy + (rb + r_terrain) * np.sin(angles)
        # Close the contour
        x_pts = np.append(x_pts, x_pts[0])
        y_pts = np.append(y_pts, y_pts[0])

        lw = 0.4 + 0.8 * t
        ax.plot(x_pts, y_pts, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines topographic mountain contour pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_topographic_mountain_contour_pattern_black_white_texture()
