import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
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


def abstract_optical_poggendorff_illusion_line_shift_pattern_black_white_texture():
    """Tweak: Parallel diagonal lines interrupted by vertical solid bars (Poggendorff optical illusion)."""
    fig, ax = setup_ax()
    
    n_lines = 40
    y_starts = np.linspace(-30, 100, n_lines)
    
    # Draw solid vertical masking bar
    bar1 = Rectangle((40, 0), 20, 100, fill=True, facecolor="black")
    ax.add_patch(bar1)
    
    for y0 in y_starts:
        # Diagonal lines crossing at 45 degrees
        ax.plot([0, 100], [y0, y0 + 100], color="black", linewidth=1.2)

    save(fig, "abstract optical poggendorff illusion line shift pattern black white texture")


if __name__ == "__main__":
    abstract_optical_poggendorff_illusion_line_shift_pattern_black_white_texture()
