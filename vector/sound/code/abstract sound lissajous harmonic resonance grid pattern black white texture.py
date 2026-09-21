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
    ax.set_xlim(-0.7, 2.7)
    ax.set_ylim(-0.7, 2.7)
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


def abstract_sound_lissajous_harmonic_resonance_grid_pattern_black_white_texture():
    """Generates a 3x3 grid of harmonically tuned Lissajous curves."""
    fig, ax = setup_ax()
    
    t = np.linspace(0, 2 * np.pi, 1000)
    
    for row in range(3):
        for col in range(3):
            # Frequency ratios change with grid position
            a = col + 1
            b = row + 2
            delta = (col + row) * np.pi / 4
            
            x_curve = col + 0.4 * np.sin(a * t + delta)
            y_curve = row + 0.4 * np.sin(b * t)
            
            # Draw primary curve
            ax.plot(x_curve, y_curve, color="black", linewidth=1.2)
            
            # Draw concentric echo curves for parallel line effect
            for scale in [0.9, 0.8, 0.7, 0.6]:
                x_echo = col + 0.4 * scale * np.sin(a * t + delta)
                y_echo = row + 0.4 * scale * np.sin(b * t)
                ax.plot(x_echo, y_echo, color="black", linewidth=0.6, alpha=0.7)

    save(fig, "abstract sound lissajous harmonic resonance grid pattern black white texture")


if __name__ == "__main__":
    abstract_sound_lissajous_harmonic_resonance_grid_pattern_black_white_texture()
