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


def abstract_dynamic_liquid_fluid_vortex_dual_core_pattern_black_white_texture():
    """Tweak: Dynamic liquid flow swirling around dual vortex cores."""
    fig, ax = setup_ax()
    
    n_lines = 40
    t = np.linspace(0, 2 * np.pi, 500)
    
    for i in range(n_lines):
        r_base = 4.0 + i * 1.1
        
        # Dual vortex cores at (35, 50) and (65, 50)
        swirl1 = 1.5 * np.sin(2 * t)
        swirl2 = 1.5 * np.cos(2 * t)
        
        x1 = 35 + (r_base + swirl1) * np.cos(t)
        y1 = 50 + (r_base + swirl1) * np.sin(t)
        
        x2 = 65 + (r_base + swirl2) * np.cos(t)
        y2 = 50 + (r_base + swirl2) * np.sin(t)
        
        ax.plot(x1, y1, color="black", linewidth=0.8)
        ax.plot(x2, y2, color="black", linewidth=0.8)

    save(fig, "abstract dynamic liquid fluid vortex dual core pattern black white texture")


if __name__ == "__main__":
    abstract_dynamic_liquid_fluid_vortex_dual_core_pattern_black_white_texture()
