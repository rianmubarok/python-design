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


def abstract_parallel_lines_black_hole_accretion_disk_horizon_pattern_black_white_texture():
    """
    Wild: Horizontal parallel lines bent around a simulated black hole.
    Gravitational lensing wraps lines around a central void (event horizon).
    Lines closest to the centre get extremely curved; an empty circle
    represents the event horizon where no lines survive.
    """
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    event_horizon_r = 8.0   # radius of the empty void
    lensing_k = 650.0       # gravitational lensing strength

    n_lines = 100
    x_base = np.linspace(-5, 105, 1200)

    y_positions = np.linspace(-5, 105, n_lines)

    for y0 in y_positions:
        x_warped = np.zeros_like(x_base)
        y_warped = np.zeros_like(x_base)

        for j, xi in enumerate(x_base):
            dx = xi - cx
            dy = y0 - cy
            r = np.sqrt(dx * dx + dy * dy)

            if r < event_horizon_r:
                # Inside event horizon: swallowed
                x_warped[j] = np.nan
                y_warped[j] = np.nan
                continue

            # Gravitational deflection: bends lines toward the mass
            # Deflection angle proportional to 1/r^2 (Schwarzschild-like)
            deflection = lensing_k / (r * r)
            deflection = min(deflection, np.pi * 0.9)  # cap at ~162°

            # Direction from point toward centre
            angle_to_centre = np.arctan2(dy, dx)

            # Apply deflection: shift the point toward the centre's tangent
            # The deflection rotates the displacement vector toward the centre
            cos_d = np.cos(deflection)
            sin_d = np.sin(deflection)

            # Rotate outward displacement slightly toward centre
            new_dx = dx * cos_d + dy * sin_d
            new_dy = -dx * sin_d + dy * cos_d

            # Scale to maintain similar radius (pure bending, not compression)
            new_r = np.sqrt(new_dx * new_dx + new_dy * new_dy)
            if new_r > 0:
                scale = r / new_r
                new_dx *= scale
                new_dy *= scale

            x_warped[j] = cx + new_dx
            y_warped[j] = cy + new_dy

        mask = (x_warped < -6) | (x_warped > 106) | (y_warped < -6) | (y_warped > 106)
        x_warped = np.where(mask, np.nan, x_warped)
        y_warped = np.where(mask, np.nan, y_warped)

        # Thicker lines near the event horizon region
        min_dist = abs(y0 - cy)
        if min_dist < event_horizon_r * 3:
            lw = 0.8 + 0.6 * (1 - min_dist / (event_horizon_r * 3))
        else:
            lw = 0.4

        ax.plot(x_warped, y_warped, color="black", linewidth=lw,
                solid_capstyle="round")

    # Draw the event horizon circle as a subtle reference
    theta_h = np.linspace(0, 2 * np.pi, 300)
    ax.fill(cx + event_horizon_r * np.cos(theta_h),
            cy + event_horizon_r * np.sin(theta_h),
            color="white", zorder=5)

    save(fig, "abstract parallel lines black hole accretion disk horizon pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_black_hole_accretion_disk_horizon_pattern_black_white_texture()
