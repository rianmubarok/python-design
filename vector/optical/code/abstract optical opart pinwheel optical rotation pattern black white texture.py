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


def abstract_optical_opart_pinwheel_optical_rotation_pattern_black_white_texture():
    """Tweak: Pinwheel of alternating line density that creates motion illusion when viewed."""
    fig, ax = setup_ax()
    
    n_spokes = 60
    t = np.linspace(0, 45, 200)
    
    for i in range(n_spokes):
        base_angle = i * 2 * np.pi / n_spokes
        
        # Spiral twist
        angle = base_angle + 0.05 * t
        
        x = 50 + t * np.cos(angle)
        y = 50 + t * np.sin(angle)
        
        lw = 0.5 if i % 2 == 0 else 1.8
        ax.plot(x, y, color="black", linewidth=lw)

    save(fig, "abstract optical opart pinwheel optical rotation pattern black white texture")


if __name__ == "__main__":
    abstract_optical_opart_pinwheel_optical_rotation_pattern_black_white_texture()
