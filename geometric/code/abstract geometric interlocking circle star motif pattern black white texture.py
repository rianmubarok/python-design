import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
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


def abstract_geometric_interlocking_circle_star_motif_pattern_black_white_texture():
    """Tweak: Interlocking geometric circle arcs forming a star motif."""
    fig, ax = setup_ax()
    
    n_petals = 12
    r_center = 25.0
    
    for i in range(n_petals):
        angle = i * 2 * np.pi / n_petals
        cx = 50 + r_center * np.cos(angle)
        cy = 50 + r_center * np.sin(angle)
        
        # Interlocking concentric arcs
        for r in [10, 18, 26]:
            arc = Arc((cx, cy), 2*r, 2*r, angle=0, theta1=0, theta2=360, color="black", linewidth=1.0)
            ax.add_patch(arc)

    save(fig, "abstract geometric interlocking circle star motif pattern black white texture")


if __name__ == "__main__":
    abstract_geometric_interlocking_circle_star_motif_pattern_black_white_texture()
