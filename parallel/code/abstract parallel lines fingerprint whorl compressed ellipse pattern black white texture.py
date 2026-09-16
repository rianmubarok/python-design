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


def abstract_parallel_lines_fingerprint_whorl_compressed_ellipse_pattern_black_white_texture():
    """
    Tweak of fingerprint whorl — squashed into a 2:1 ellipse (landscape).
    Creates a stretched, wide fingerprint texture.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_lines = 85
    x_base = np.linspace(-5, 105, 900)

    # Elliptical whorl parameters
    # Use an elliptical distance metric: stretch y by 2x
    aspect_x = 1.0   # normal in x
    aspect_y = 2.0    # compressed in y (making landscape ellipse)

    whorl_k = 220.0
    min_r = 2.0

    y_positions = np.linspace(-5, 105, n_lines)

    for y0 in y_positions:
        x_warped = np.zeros_like(x_base)
        y_warped = np.zeros_like(x_base)

        for j, xi in enumerate(x_base):
            dx = (xi - cx) * aspect_x
            dy = (y0 - cy) * aspect_y
            r = np.sqrt(dx * dx + dy * dy)
            r = max(r, min_r)

            # Rotation angle based on elliptical distance
            theta = np.deg2rad(whorl_k / r)

            cos_t = np.cos(theta)
            sin_t = np.sin(theta)

            # Rotate in elliptical space, then map back
            new_dx = dx * cos_t - dy * sin_t
            new_dy = dx * sin_t + dy * cos_t

            x_warped[j] = cx + new_dx / aspect_x
            y_warped[j] = cy + new_dy / aspect_y

        mask = (x_warped < -6) | (x_warped > 106) | (y_warped < -6) | (y_warped > 106)
        x_warped = np.where(mask, np.nan, x_warped)
        y_warped = np.where(mask, np.nan, y_warped)

        dist_to_cy = abs(y0 - cy) / 55.0
        lw = 0.3 + 0.7 * (1 - min(dist_to_cy, 1.0) ** 0.6)

        ax.plot(x_warped, y_warped, color="black", linewidth=lw,
                solid_capstyle="round")

    save(fig, "abstract parallel lines fingerprint whorl compressed ellipse pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_fingerprint_whorl_compressed_ellipse_pattern_black_white_texture()
