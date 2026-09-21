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


def abstract_parallel_lines_celtic_braid_triaxial_pattern_black_white_texture():
    """Wild: three diagonal families interlaced at 60° like a Celtic triaxial braid"""
    fig, ax = setup_ax()

    # Three line families at 0°, 60°, 120°
    angles_deg = [0, 60, 120]
    n_lines_per_family = 26
    spacing = 5.2
    lw = 0.9
    length = 180  # long enough to cross canvas diagonally

    for ang_deg in angles_deg:
        ang = np.radians(ang_deg)
        # Direction vector
        dx, dy = np.cos(ang), np.sin(ang)
        # Perpendicular vector
        px, py = -dy, dx

        for k in range(-n_lines_per_family, n_lines_per_family + 1):
            # Offset from centre along perpendicular
            offset = k * spacing
            # Line midpoint
            mx = 50.0 + offset * px
            my = 50.0 + offset * py
            # Start and end
            x0 = mx - length * dx
            y0 = my - length * dy
            x1 = mx + length * dx
            y1 = my + length * dy

            # Clip to canvas using parametric form
            # x = x0 + t*(x1-x0), y = y0 + t*(y1-y0), t in [0,1]
            pts_x = np.array([x0, x1])
            pts_y = np.array([y0, y1])

            # Simple clip: sample along line and mask
            ts = np.linspace(0, 1, 600)
            xs = x0 + ts * (x1 - x0)
            ys = y0 + ts * (y1 - y0)
            mask = (xs >= -5) & (xs <= 105) & (ys >= -5) & (ys <= 105)
            xs = np.where(mask, xs, np.nan)
            ys = np.where(mask, ys, np.nan)
            ax.plot(xs, ys, color="black", linewidth=lw, solid_capstyle="round", alpha=0.8)

    save(fig, "abstract parallel lines celtic braid triaxial pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_celtic_braid_triaxial_pattern_black_white_texture()
