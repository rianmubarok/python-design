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


def abstract_parallel_lines_seismic_fault_shear_slip_offset_pattern_black_white_texture():
    """
    Horizontal parallel lines that are cleanly offset at a diagonal fault line,
    as if tectonic plates slipped past each other (strike-slip fault).
    The fault runs diagonally. Each side shifts in opposite directions.
    Near the fault, lines smoothly transition showing the elastic rebound zone.
    """
    fig, ax = setup_ax()

    n_lines = 90
    # Fault line: diagonal from (30, -5) to (70, 105)
    # Parametric: x_fault(y) = 30 + (70-30)/(105-(-5)) * (y - (-5))
    fault_slope = (70 - 30) / (105 + 5)   # dx/dy
    fault_origin_y = -5
    fault_origin_x = 30

    def fault_x(y):
        return fault_origin_x + fault_slope * (y - fault_origin_y)

    # Total horizontal slip offset
    slip = 18.0
    # Transition zone half-width (in canvas units)
    transition = 7.0

    x = np.linspace(-5, 105, 800)
    y_positions = np.linspace(-5, 105, n_lines)

    for y0 in y_positions:
        y = np.full_like(x, y0)

        # For each x, compute signed distance from fault
        fx = fault_x(y0)
        signed_dist = x - fx  # positive = right of fault

        # Smooth tanh transition for the slip offset (applied to y)
        # On left: shift up by slip/2, on right: shift down by slip/2
        smooth = np.tanh(signed_dist / transition)
        y_shifted = y - smooth * (slip / 2)

        # Mask out-of-canvas
        mask = (y_shifted < -6) | (y_shifted > 106)
        y_shifted = np.where(mask, np.nan, y_shifted)

        # Line weight thicker near fault (stress concentration)
        dist_arr = np.abs(signed_dist)
        near_fault = np.exp(-dist_arr / transition)
        mean_near = float(np.nanmean(near_fault))
        lw = 0.4 + 0.85 * mean_near

        ax.plot(x, y_shifted, color="black", linewidth=lw,
                solid_capstyle="round")

    save(fig, "abstract parallel lines seismic fault shear slip offset pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_seismic_fault_shear_slip_offset_pattern_black_white_texture()
