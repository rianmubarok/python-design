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


def abstract_parallel_lines_slit_diffraction_ripple_fan_wide_aperture_pattern_black_white_texture():
    """
    Tweak of slit diffraction: wider slit (12 units instead of 4),
    lower spread angle (35°), more lines pass through — gentler, wider fan.
    """
    fig, ax = setup_ax()

    slit_x = 50.0
    slit_y = 50.0
    slit_half = 12.0  # widened from 4.0

    n_lines = 80
    x_left = np.linspace(-5, slit_x, 400)
    x_right = np.linspace(slit_x, 108, 600)

    y_starts = np.linspace(-5, 105, n_lines)

    for i, y0 in enumerate(y_starts):
        # ----- LEFT SIDE -----
        if y0 < slit_y - slit_half:
            target_y = slit_y - slit_half
        elif y0 > slit_y + slit_half:
            target_y = slit_y + slit_half
        else:
            target_y = y0

        t = (x_left - (-5)) / (slit_x - (-5))
        compress = t ** 2
        y_left = y0 + (target_y - y0) * compress

        lw_left = 0.55
        ax.plot(x_left, y_left, color="black", linewidth=lw_left,
                solid_capstyle="round")

        # ----- RIGHT SIDE -----
        if abs(y0 - slit_y) > slit_half * 1.05:
            continue

        norm = (y0 - slit_y) / slit_half
        max_spread_angle = 35.0  # reduced from 62°

        angle_deg = norm * max_spread_angle
        angle_rad = np.deg2rad(angle_deg)

        t2 = (x_right - slit_x) / (108 - slit_x)

        sinc_arg = np.pi * norm * 2.5 if norm != 0 else 1e-9
        intensity = (np.sin(sinc_arg) / sinc_arg) ** 2 if norm != 0 else 1.0
        intensity = max(0.05, intensity)

        y_fan = slit_y + np.tan(angle_rad) * (x_right - slit_x)
        ripple_freq = 0.10
        ripple_amp = 2.5 * (1 - t2) * intensity
        y_right = y_fan + ripple_amp * np.sin(2 * np.pi * ripple_freq * x_right)

        mask = (y_right < -6) | (y_right > 106)
        y_right = np.where(mask, np.nan, y_right)

        lw_right = 0.3 + 0.8 * intensity
        ax.plot(x_right, y_right, color="black", linewidth=lw_right,
                solid_capstyle="round")

    save(fig, "abstract parallel lines slit diffraction ripple fan wide aperture pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_slit_diffraction_ripple_fan_wide_aperture_pattern_black_white_texture()
