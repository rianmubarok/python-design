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


def abstract_dynamic_wave_distortion_concentric_circle_offset_pattern_black_white_texture():
    """Tweak: Concentric circles with dynamic wave ripple offsets along both X and Y axes."""
    fig, ax = setup_ax()
    
    n_circles = 40
    t = np.linspace(0, 2 * np.pi, 300)
    
    for i in range(n_circles):
        r = 2.0 + i * 1.1
        
        # Dynamic X & Y wave offsets
        ox = 3.0 * np.sin(i * 0.4)
        oy = 3.0 * np.cos(i * 0.4)
        
        x = 50 + ox + r * np.cos(t)
        y = 50 + oy + r * np.sin(t)
        
        lw = 0.5 + 0.4 * (1 - i / n_circles)
        ax.plot(x, y, color="black", linewidth=lw)

    save(fig, "abstract dynamic wave distortion concentric circle offset pattern black white texture")


if __name__ == "__main__":
    abstract_dynamic_wave_distortion_concentric_circle_offset_pattern_black_white_texture()
