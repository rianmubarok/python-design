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
    Pseudo Perlin / Turbulent Fluid Flow.
    We create a chaotic vector field using a sum of overlapping sine waves 
    at various scales and angles. The parallel lines act as streamlines
    bending smoothly through this turbulent flow field.
    """
    fig, ax = setup_ax()

    n_lines = 100
    n_pts = 600

    # Define frequencies, amplitudes, and phases for the pseudo-noise field
    rng = np.random.default_rng(42)
    n_octaves = 4
    octaves = []
    for i in range(n_octaves):
        freq = 0.02 * (2 ** i)
        amp = 4.0 / (2 ** i)
        phase_x = rng.uniform(0, 2 * np.pi)
        phase_y = rng.uniform(0, 2 * np.pi)
        dir_x = rng.uniform(-1, 1)
        dir_y = rng.uniform(-1, 1)
        # Normalize direction
        length = np.sqrt(dir_x**2 + dir_y**2)
        dir_x /= length
        dir_y /= length
        octaves.append((freq, amp, phase_x, phase_y, dir_x, dir_y))

    for i in range(n_lines):
        y0 = -5 + 110 * i / (n_lines - 1)
        x_base = np.linspace(-5, 105, n_pts)
        
        x_out = np.copy(x_base)
        y_out = np.full(n_pts, y0)

        # Apply displacement based on the vector field
        for freq, amp, px, py, dx, dy in octaves:
            # Displacement depends on position
            displacement = np.sin(x_base * freq * dx + px) * np.cos(y0 * freq * dy + py)
            y_out += displacement * amp
            x_out += displacement * amp * 0.3  # Slight horizontal dragging

        ax.plot(x_out, y_out, color="black", linewidth=0.5, solid_capstyle="round")

    save(fig, "abstract parallel lines pseudo perlin turbulent flow pattern black white texture")


if __name__ == "__main__":
    draw()
