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
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
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


def abstract_grid_tessellation_hyperbolic_disk_poincare_disk_grid_pattern_black_white_texture():
    """Tweak: Poincaré hyperbolic disk grid where lines curve toward the boundary."""
    fig, ax = setup_ax()
    
    # Outer circle boundary
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(t), np.sin(t), color="black", linewidth=1.8)
    
    # Hyperbolic orthogonal circles
    radii = [0.25, 0.5, 0.75, 0.9, 0.96]
    for r in radii:
        ax.plot(r * np.cos(t), r * np.sin(t), color="black", linewidth=0.8)
        
    n_spokes = 16
    for i in range(n_spokes):
        angle = i * 2 * np.pi / n_spokes
        ax.plot([0, np.cos(angle)], [0, np.sin(angle)], color="black", linewidth=0.8)

    save(fig, "abstract grid tessellation hyperbolic disk poincare disk grid pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_hyperbolic_disk_poincare_disk_grid_pattern_black_white_texture()
