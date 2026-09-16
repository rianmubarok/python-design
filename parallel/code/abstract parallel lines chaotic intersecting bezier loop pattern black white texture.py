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


def abstract_parallel_lines_chaotic_intersecting_bezier_loop_pattern_black_white_texture():
    """Wild: Complex chaotic intersecting smooth curves simulating multi-dimensional parallel flow."""
    fig, ax = setup_ax()
    
    n_lines = 40
    t = np.linspace(0, 2 * np.pi, 500)
    
    for i in range(n_lines):
        # Base circular path
        r_base = 10 + i * 1.5
        
        # Add high-frequency chaotic displacements
        freq1 = 3 + np.random.rand() * 2
        freq2 = 5 + np.random.rand() * 3
        
        amp1 = 15 * np.sin(i * 0.1)
        amp2 = 8 * np.cos(i * 0.15)
        
        r = r_base + amp1 * np.sin(freq1 * t) + amp2 * np.cos(freq2 * t)
        
        # Convert to polar, then add a drifting center
        drift_x = 50 + 10 * np.sin(i * 0.2)
        drift_y = 50 + 10 * np.cos(i * 0.2)
        
        x = drift_x + r * np.cos(t)
        y = drift_y + r * np.sin(t)
        
        lw = 0.4 + 0.4 * (np.random.rand())
        
        ax.plot(x, y, color="black", linewidth=lw, alpha=0.9)
        
    save(fig, "abstract parallel lines chaotic intersecting bezier loop pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_chaotic_intersecting_bezier_loop_pattern_black_white_texture()
