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


def abstract_parallel_lines_interference_two_vortex_dipole_pattern_black_white_texture():
    """
    Wild: Two counter-rotating vortices side by side (dipole).
    Left vortex spins clockwise, right spins counter-clockwise.
    Between them, lines get pulled in opposite directions creating
    a chaotic interference zone. Edges remain calm.
    """
    fig, ax = setup_ax()

    # Two vortex centres
    v1_x, v1_y = 30.0, 50.0   # left vortex (clockwise)
    v2_x, v2_y = 70.0, 50.0   # right vortex (counter-clockwise)

    vortex_k1 = 220.0   # strength of left vortex
    vortex_k2 = -220.0  # negative = opposite rotation
    min_r = 2.5

    n_lines = 85
    x_base = np.linspace(-5, 105, 900)
    y_positions = np.linspace(-5, 105, n_lines)

    for y0 in y_positions:
        x_warped = np.zeros_like(x_base)
        y_warped = np.zeros_like(x_base)

        for j, xi in enumerate(x_base):
            # Displacement from vortex 1
            dx1 = xi - v1_x
            dy1 = y0 - v1_y
            r1 = max(np.sqrt(dx1 * dx1 + dy1 * dy1), min_r)
            theta1 = np.deg2rad(vortex_k1 / r1)

            # Displacement from vortex 2
            dx2 = xi - v2_x
            dy2 = y0 - v2_y
            r2 = max(np.sqrt(dx2 * dx2 + dy2 * dy2), min_r)
            theta2 = np.deg2rad(vortex_k2 / r2)

            # Apply vortex 1 rotation
            cos1 = np.cos(theta1)
            sin1 = np.sin(theta1)
            mid_dx = dx1 * cos1 - dy1 * sin1
            mid_dy = dx1 * sin1 + dy1 * cos1
            mid_x = v1_x + mid_dx
            mid_y = v1_y + mid_dy

            # Then apply vortex 2 rotation on the result
            dx2b = mid_x - v2_x
            dy2b = mid_y - v2_y
            cos2 = np.cos(theta2)
            sin2 = np.sin(theta2)
            final_dx = dx2b * cos2 - dy2b * sin2
            final_dy = dx2b * sin2 + dy2b * cos2

            x_warped[j] = v2_x + final_dx
            y_warped[j] = v2_y + final_dy

        mask = (x_warped < -6) | (x_warped > 106) | (y_warped < -6) | (y_warped > 106)
        x_warped = np.where(mask, np.nan, x_warped)
        y_warped = np.where(mask, np.nan, y_warped)

        # Line weight varies with proximity to either vortex
        d1 = abs(y0 - v1_y) / 55.0
        d2 = abs(y0 - v2_y) / 55.0
        proximity = min(d1, d2)
        lw = 0.3 + 0.7 * (1 - min(proximity, 1.0) ** 0.6)

        ax.plot(x_warped, y_warped, color="black", linewidth=lw,
                solid_capstyle="round")

    save(fig, "abstract parallel lines interference two vortex dipole pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_interference_two_vortex_dipole_pattern_black_white_texture()
