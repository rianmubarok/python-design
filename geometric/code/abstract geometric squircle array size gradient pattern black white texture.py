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


def abstract_geometric_squircle_array_size_gradient_pattern_black_white_texture():
    """Tweak: Array of squircles scaling in size from left to right."""
    fig, ax = setup_ax()
    
    n_cols = 8
    n_rows = 8
    dx = 100 / n_cols
    dy = 100 / n_rows
    t_vals = np.linspace(0, 2 * np.pi, 200)
    
    for r in range(n_rows):
        for c in range(n_cols):
            cx = (c + 0.5) * dx
            cy = (r + 0.5) * dy
            
            # Size gradient from left to right
            scale = 0.3 + 0.6 * (c / (n_cols - 1))
            r_base = dx * 0.45 * scale
            p = 3.5  # Squircle exponent
            
            cos_t = np.cos(t_vals)
            sin_t = np.sin(t_vals)
            
            x = cx + r_base * np.sign(cos_t) * (np.abs(cos_t) ** (2 / p))
            y = cy + r_base * np.sign(sin_t) * (np.abs(sin_t) ** (2 / p))
            
            ax.plot(x, y, color="black", linewidth=1.0)

    save(fig, "abstract geometric squircle array size gradient pattern black white texture")


if __name__ == "__main__":
    abstract_geometric_squircle_array_size_gradient_pattern_black_white_texture()
