import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
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
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
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


def abstract_optical_kanizsa_square_triangle_negative_space_pattern_black_white_texture():
    """Tweak: Subjective contour illusion (Kanizsa Square) using concentric Pac-Man cutouts."""
    fig, ax = setup_ax()
    
    # 4 Pac-Man circles at corners of a square (30,30), (70,30), (70,70), (30,70)
    centers = [(30, 30), (70, 30), (70, 70), (30, 70)]
    angles = [(0, 270), (90, 360), (180, 450), (270, 540)]
    
    for (cx, cy), (t1, t2) in zip(centers, angles):
        # Draw concentric rings inside Pac-Man
        for r in np.linspace(3, 16, 8):
            w = Wedge((cx, cy), r, t1, t2, width=1.0, fill=True, facecolor="black")
            ax.add_patch(w)

    save(fig, "abstract optical kanizsa square triangle negative space pattern black white texture")


if __name__ == "__main__":
    abstract_optical_kanizsa_square_triangle_negative_space_pattern_black_white_texture()
