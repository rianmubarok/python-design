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


def abstract_dynamic_squircle_morph_corner_radius_sweep_pattern_black_white_texture():
    """Tweak: Squircles whose corner radii sweep dynamically from sharp chamfers to smooth round arcs."""
    fig, ax = setup_ax()
    
    n_shapes = 36
    t_vals = np.linspace(0, 2 * np.pi, 300)
    
    for i in range(n_shapes):
        r_base = 48 - i * 1.25
        if r_base <= 2:
            break
            
        # Superellipse exponent sweeps from 10.0 (sharp) to 2.0 (smooth circle)
        p = 2.0 + 8.0 * (i / n_shapes)
        
        cos_t = np.cos(t_vals)
        sin_t = np.sin(t_vals)
        
        x = 50 + r_base * np.sign(cos_t) * (np.abs(cos_t) ** (2 / p))
        y = 50 + r_base * np.sign(sin_t) * (np.abs(sin_t) ** (2 / p))
        
        ax.plot(x, y, color="black", linewidth=0.8)

    save(fig, "abstract dynamic squircle morph corner radius sweep pattern black white texture")


if __name__ == "__main__":
    abstract_dynamic_squircle_morph_corner_radius_sweep_pattern_black_white_texture()
