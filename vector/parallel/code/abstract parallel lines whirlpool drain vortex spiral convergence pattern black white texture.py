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
    print(f"Saved: {jpg_path} | {svg_path}")


def abstract_parallel_lines_whirlpool_drain_vortex_spiral_convergence_pattern_black_white_texture():
    """
    Horizontal parallel lines distorted by a whirlpool/drain vortex:
    each point is rotated around the centre by an angle inversely proportional
    to its radius — lines far from centre are nearly straight; lines near the
    centre spiral tightly inward like water draining into a sink.
    This is a pure rotational warp (not radial compression), giving spiral arms.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_lines = 85
    x_base = np.linspace(-5, 105, 900)

    # Vortex strength: how many degrees to rotate at r=1
    vortex_k = 280.0   # degrees * canvas_units
    min_r = 1.5         # avoid singularity

    y_positions = np.linspace(-5, 105, n_lines)

    for y0 in y_positions:
        x_warped = np.zeros_like(x_base)
        y_warped = np.zeros_like(x_base)

        for j, xi in enumerate(x_base):
            dx = xi - cx
            dy = y0 - cy
            r = np.sqrt(dx * dx + dy * dy)
            r = max(r, min_r)

            # Rotation angle: stronger near centre
            theta = np.deg2rad(vortex_k / r)

            # Rotate (dx, dy) by theta
            cos_t = np.cos(theta)
            sin_t = np.sin(theta)
            new_dx = dx * cos_t - dy * sin_t
            new_dy = dx * sin_t + dy * cos_t

            x_warped[j] = cx + new_dx
            y_warped[j] = cy + new_dy

        # Mask out-of-canvas
        mask = (x_warped < -6) | (x_warped > 106) | (y_warped < -6) | (y_warped > 106)
        x_warped = np.where(mask, np.nan, x_warped)
        y_warped = np.where(mask, np.nan, y_warped)

        # Line weight: thicker near drain center
        dist_to_cx = abs(y0 - cy) / 55.0
        lw = 0.35 + 0.75 * (1 - dist_to_cx ** 0.6)

        ax.plot(x_warped, y_warped, color="black", linewidth=lw,
                solid_capstyle="round")

    save(fig, "abstract parallel lines whirlpool drain vortex spiral convergence pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_whirlpool_drain_vortex_spiral_convergence_pattern_black_white_texture()
