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


def abstract_optical_zollner_illusion_wave_hatched_line_pattern_black_white_texture():
    """Optical experiment: Zöllner illusion with wave-modulated main lines and alternating angle hatch marks causing illusory line tilt."""
    fig, ax = setup_ax()

    n_lines = 28
    y_coords = np.linspace(-45, 45, n_lines)

    for i, y_base in enumerate(y_coords):
        # Wave baseline path
        x_pts = np.linspace(-48, 48, 200)
        wave_y = y_base + 1.2 * np.sin(x_pts * 0.12 + i * 0.3)

        # Plot main horizontal/wave line
        ax.plot(x_pts, wave_y, color="black", linewidth=2.5)

        # Hatch mark angle alternates between lines (+45 deg and -45 deg)
        base_hatch_angle = np.radians(40 if i % 2 == 0 else -40)
        hatch_length = 3.2
        num_hatches = 35

        hatch_x_centers = np.linspace(-46, 46, num_hatches)
        for hx in hatch_x_centers:
            hy = y_base + 1.2 * np.sin(hx * 0.12 + i * 0.3)
            # Modulate angle slightly along the length
            local_angle = base_hatch_angle + 0.15 * np.cos(hx * 0.1)

            dx = (hatch_length / 2) * np.cos(local_angle)
            dy = (hatch_length / 2) * np.sin(local_angle)

            ax.plot(
                [hx - dx, hx + dx],
                [hy - dy, hy + dy],
                color="black",
                linewidth=1.8,
            )

    save(
        fig,
        "abstract optical zollner illusion wave hatched line pattern black white texture",
    )


if __name__ == "__main__":
    abstract_optical_zollner_illusion_wave_hatched_line_pattern_black_white_texture()
