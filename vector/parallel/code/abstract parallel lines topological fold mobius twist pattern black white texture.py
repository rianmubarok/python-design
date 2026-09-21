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


def abstract_parallel_lines_topological_fold_mobius_twist_pattern_black_white_texture():
    """
    Wild: Parallel lines undergo a continuous 180° twist across the canvas.
    Lines that start horizontal on the left gradually rotate and cross over
    each other, arriving at the right side in reversed vertical order.
    Creates a Möbius-strip-like crossing illusion in 2D.
    """
    fig, ax = setup_ax()

    n_lines = 50
    n_pts = 800
    x_base = np.linspace(-5, 105, n_pts)

    # Each line starts at y_start on the left edge and ends at y_end on the right
    # y_end is the mirror of y_start around the centre (Möbius flip)
    y_starts = np.linspace(-5, 105, n_lines)
    cy = 50.0

    for idx, y0 in enumerate(y_starts):
        # Mirror target: line that starts at y0 ends at (100 - y0) effectively
        y_end = 2 * cy - y0

        # Parametric t across the canvas
        t = (x_base - (-5)) / (105 - (-5))  # 0..1

        # Smooth interpolation with a twist:
        # Use a sigmoid-like twist that creates crossings in the middle
        # Each line follows: y(t) = y0*(1-s(t)) + y_end*s(t)
        # where s(t) is a smooth step that goes 0→1

        # Add vertical sinusoidal undulation that's strongest at the twist centre
        twist_centre = 0.5
        twist_width = 0.3

        # Smooth step: using smoothstep (Hermite interpolation)
        s = np.clip((t - (twist_centre - twist_width)) / (2 * twist_width), 0, 1)
        s = s * s * (3 - 2 * s)  # smoothstep

        y_line = y0 * (1 - s) + y_end * s

        # Add a sine wave bulge in the twist zone to visualize the rotation
        bulge_env = np.exp(-((t - twist_centre) ** 2) / (2 * 0.08 ** 2))
        # Amplitude depends on distance from centre (edge lines twist more visibly)
        amp = 3.5 * abs(y0 - cy) / 55.0
        y_line += amp * bulge_env * np.sin(np.pi * t * 4 + idx * 0.15)

        mask = (y_line < -6) | (y_line > 106)
        y_line = np.where(mask, np.nan, y_line)

        # Thicker in the twist zone, thinner at edges
        lw = 0.4 + 0.5 * (1 - abs(y0 - cy) / 60.0)

        ax.plot(x_base, y_line, color="black", linewidth=lw,
                solid_capstyle="round")

    save(fig, "abstract parallel lines topological fold mobius twist pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_topological_fold_mobius_twist_pattern_black_white_texture()
