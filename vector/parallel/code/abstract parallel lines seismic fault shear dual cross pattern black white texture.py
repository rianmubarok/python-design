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


def abstract_parallel_lines_seismic_fault_shear_dual_cross_pattern_black_white_texture():
    """
    TWO diagonal fault lines crossing in an X near the centre.
    Four plates each shift in their own direction — the intersection
    creates a complex elastic rebound zone where offsets compound.
    """
    fig, ax = setup_ax()

    n_lines = 90
    x = np.linspace(-5, 105, 800)
    y_positions = np.linspace(-5, 105, n_lines)

    # Fault A: runs from bottom-left to top-right  (~30° from horizontal)
    # x_faultA(y) = 20 + 0.6*(y+5)
    def fault_a_x(y):
        return 20.0 + 0.6 * (y + 5.0)

    # Fault B: runs from top-left to bottom-right  (~-30° from horizontal)
    # x_faultB(y) = 80 - 0.6*(y+5)
    def fault_b_x(y):
        return 80.0 - 0.6 * (y + 5.0)

    slip_a = 14.0
    slip_b = 11.0
    transition = 6.0

    for y0 in y_positions:
        y = np.full_like(x, y0)

        # Fault A offset (vertical shift via tanh)
        fa_x = fault_a_x(y0)
        signed_a = x - fa_x
        smooth_a = np.tanh(signed_a / transition)

        # Fault B offset (vertical shift via tanh, opposite polarity)
        fb_x = fault_b_x(y0)
        signed_b = x - fb_x
        smooth_b = np.tanh(signed_b / transition)

        # Combine both fault offsets — they compound at the intersection
        y_shifted = y - smooth_a * (slip_a / 2) + smooth_b * (slip_b / 2)

        mask = (y_shifted < -6) | (y_shifted > 106)
        y_shifted = np.where(mask, np.nan, y_shifted)

        # Line weight: thicker near either fault
        dist_a = np.abs(signed_a)
        dist_b = np.abs(signed_b)
        near_fault = np.maximum(np.exp(-dist_a / transition), np.exp(-dist_b / transition))
        mean_near = float(np.nanmean(near_fault))
        lw = 0.35 + 0.9 * mean_near

        ax.plot(x, y_shifted, color="black", linewidth=lw,
                solid_capstyle="round")

    save(fig, "abstract parallel lines seismic fault shear dual cross pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_seismic_fault_shear_dual_cross_pattern_black_white_texture()
