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


def draw():
    """
    Concentric circles emanating from a moving source — the Doppler effect.
    Circles are compressed in the direction of motion (right) and stretched
    in the opposite direction (left). Lines remain parallel to each other
    as concentric rings but with asymmetric spacing.
    """
    fig, ax = setup_ax()

    # Source moving to the right
    source_x, source_y = 50.0, 50.0
    velocity = 0.55  # fraction of wave speed (subsonic)
    n_waves = 50

    n_pts = 500

    for i in range(n_waves):
        # Each wave was emitted at a past position
        t_emit = (n_waves - i) / n_waves  # time since emission (normalized)
        emit_x = source_x - velocity * t_emit * 60  # source was at this x
        emit_y = source_y

        # Wave has expanded by r = t_emit * wave_speed
        base_r = t_emit * 55

        if base_r < 1.0:
            continue

        theta = np.linspace(0, 2 * np.pi, n_pts)
        # Doppler shift: radius varies with angle relative to velocity direction
        # In direction of motion (theta=0, rightward): compressed
        # Opposite (theta=pi, leftward): expanded
        r_doppler = base_r  # the circle is already offset by emitting from different positions

        cx = emit_x + r_doppler * np.cos(theta)
        cy = emit_y + r_doppler * np.sin(theta)

        # Clip to viewport
        mask = (cx < -6) | (cx > 106) | (cy < -6) | (cy > 106)
        cx = np.where(mask, np.nan, cx)
        cy = np.where(mask, np.nan, cy)

        lw = 0.3 + 0.3 * (1 - t_emit)
        ax.plot(cx, cy, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines doppler redshift blueshift compression pattern black white texture")


if __name__ == "__main__":
    draw()
