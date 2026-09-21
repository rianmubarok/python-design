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


def abstract_opart_moire_interference_scroll_kinetic_pattern_black_white_texture():
    """Generates a high-density Moire interference pattern."""
    fig, ax = setup_ax()
    
    # Layer 1: Perfect radiating lines from a center point
    n_lines = 160
    t = np.linspace(0, 100, 2)
    center1_x, center1_y = 50, 50
    
    for i in range(n_lines):
        angle = (i / n_lines) * 2 * np.pi
        x_dir = np.cos(angle)
        y_dir = np.sin(angle)
        
        # Extend from center to outside the frame
        x = [center1_x, center1_x + x_dir * 100]
        y = [center1_y, center1_y + y_dir * 100]
        ax.plot(x, y, color="black", linewidth=1.5)
        
    # Layer 2: Offset radiating lines to create Moire effect
    center2_x, center2_y = 52, 52
    for i in range(n_lines):
        angle = (i / n_lines) * 2 * np.pi
        x_dir = np.cos(angle)
        y_dir = np.sin(angle)
        
        x = [center2_x, center2_x + x_dir * 100]
        y = [center2_y, center2_y + y_dir * 100]
        # Slightly thinner lines for the overlapping interference
        ax.plot(x, y, color="black", linewidth=1.0)
        
    save(fig, "abstract opart moire interference scroll kinetic pattern black white texture")


if __name__ == "__main__":
    abstract_opart_moire_interference_scroll_kinetic_pattern_black_white_texture()
