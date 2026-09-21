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


def abstract_dynamic_squircle_morph_pulse_wave_pattern_black_white_texture():
    """Tweak: Superellipse squircles pulsing dynamically between sharp squares and smooth circles."""
    fig, ax = setup_ax()
    
    n_shapes = 35
    t_vals = np.linspace(0, 2 * np.pi, 300)
    
    for i in range(n_shapes):
        r_base = 48 - i * 1.3
        if r_base <= 2:
            break
            
        # Superellipse exponent p pulses sinusoidally
        p = 2.0 + 4.0 * (0.5 * (1 + np.sin(i * 0.3)))
        
        cos_t = np.cos(t_vals)
        sin_t = np.sin(t_vals)
        
        x = 50 + r_base * np.sign(cos_t) * (np.abs(cos_t) ** (2 / p))
        y = 50 + r_base * np.sign(sin_t) * (np.abs(sin_t) ** (2 / p))
        
        lw = 0.5 + 0.3 * (1 - i / n_shapes)
        ax.plot(x, y, color="black", linewidth=lw)

    save(fig, "abstract dynamic squircle morph pulse wave pattern black white texture")


if __name__ == "__main__":
    abstract_dynamic_squircle_morph_pulse_wave_pattern_black_white_texture()
