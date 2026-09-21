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
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
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


def abstract_optical_lissajous_optical_wave_phase_shift_grid_pattern_black_white_texture():
    """Optical experiment: Lissajous harmonic curves overlaid with phase-shifted optical grid lines."""
    fig, ax = setup_ax()

    # Draw background Lissajous harmonic resonance web
    t = np.linspace(0, 2 * np.pi, 2000)
    freq_pairs = [(3, 4), (5, 6), (7, 8), (4, 7)]

    for idx, (fa, fb) in enumerate(freq_pairs):
        delta = idx * np.pi / 4
        scale = 44.0 - idx * 6.0

        x_liss = scale * np.sin(fa * t + delta)
        y_liss = scale * np.cos(fb * t)

        ax.plot(
            x_liss, y_liss, color="black", linewidth=1.5, alpha=0.65
        )

    # Superimpose phase-shifted vertical & horizontal optical lines
    x_grid = np.linspace(-46, 46, 36)
    y_pts = np.linspace(-46, 46, 300)

    for i, x_base in enumerate(x_grid):
        # Phase shift depends on distance to center and Lissajous frequency
        shift = 2.4 * np.sin(y_pts * 0.18 + i * 0.4)
        ax.plot(x_base + shift, y_pts, color="black", linewidth=1.2)

    y_grid = np.linspace(-46, 46, 36)
    x_pts = np.linspace(-46, 46, 300)

    for j, y_base in enumerate(y_grid):
        shift = 2.4 * np.cos(x_pts * 0.18 + j * 0.4)
        ax.plot(x_pts, y_base + shift, color="black", linewidth=1.2)

    save(
        fig,
        "abstract optical lissajous optical wave phase shift grid pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_lissajous_optical_wave_phase_shift_grid_pattern_black_white_texture()
