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


def abstract_parallel_lines_tidal_force_spaghettification_stretch_pattern_black_white_texture():
    """
    Wild: Horizontal parallel lines enter from the top uniformly, but get
    progressively stretched and narrowed toward a singularity at the bottom.
    Lines compress horizontally (crowd together) while elongating vertically
    (stretch apart) — simulating tidal spaghettification near a gravitational
    singularity.
    """
    fig, ax = setup_ax()

    # Singularity position (bottom-centre)
    sx, sy = 50.0, -10.0
    n_lines = 70
    n_pts = 800

    # Horizontal lines entering from the top
    y_starts = np.linspace(105, -5, n_lines)

    for idx, y0 in enumerate(y_starts):
        x_base = np.linspace(-5, 105, n_pts)
        y_base = np.full(n_pts, y0)

        x_warped = np.zeros(n_pts)
        y_warped = np.zeros(n_pts)

        for j in range(n_pts):
            xi = x_base[j]
            yi = y_base[j]

            # Distance from singularity
            dx = xi - sx
            dy = yi - sy
            r = np.sqrt(dx * dx + dy * dy)
            r = max(r, 3.0)

            # Tidal stretching: compress x toward singularity column,
            # stretch y away from singularity (vertical elongation)
            # Strength increases as y decreases (closer to singularity)
            proximity = max(0, 1.0 - (yi - sy) / 120.0)  # 0 at top, ~1 near bottom
            tidal_strength = proximity ** 2.5

            # Horizontal compression: x converges toward sx
            x_compress = 1.0 - 0.85 * tidal_strength * np.exp(-abs(dx) / 40.0)
            new_x = sx + dx * x_compress

            # Vertical stretching: lines near the bottom spread apart more
            y_stretch = 1.0 + 2.0 * tidal_strength
            new_y = sy + dy * y_stretch

            x_warped[j] = new_x
            y_warped[j] = new_y

        mask = (x_warped < -6) | (x_warped > 106) | (y_warped < -6) | (y_warped > 106)
        x_warped = np.where(mask, np.nan, x_warped)
        y_warped = np.where(mask, np.nan, y_warped)

        # Lines get thinner as they stretch (spaghettification)
        t = idx / max(n_lines - 1, 1)
        lw = 0.9 - 0.5 * t  # thicker at top, thinner at bottom

        ax.plot(x_warped, y_warped, color="black", linewidth=lw,
                solid_capstyle="round")

    save(fig, "abstract parallel lines tidal force spaghettification stretch pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_tidal_force_spaghettification_stretch_pattern_black_white_texture()
