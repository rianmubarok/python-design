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


def abstract_dynamic_Doppler_shift_radial_expansion_pattern_black_white_texture():
    """Tweak: Radial lines experiencing a Doppler compression density shift."""
    fig, ax = setup_ax()
    
    n_spokes = 90
    for i in range(n_spokes):
        # Angle compressed on right side (Doppler redshift/blueshift effect)
        t = (i / n_spokes) * 2 * np.pi
        angle = t + 0.4 * np.sin(t)
        
        x = [50, 50 + 45 * np.cos(angle)]
        y = [50, 50 + 45 * np.sin(angle)]
        
        lw = 0.5 + 1.0 * (0.5 * (1 + np.cos(angle)))
        ax.plot(x, y, color="black", linewidth=lw)

    save(fig, "abstract dynamic Doppler shift radial expansion pattern black white texture")


if __name__ == "__main__":
    abstract_dynamic_Doppler_shift_radial_expansion_pattern_black_white_texture()
