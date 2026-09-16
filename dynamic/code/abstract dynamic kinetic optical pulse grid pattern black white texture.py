import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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


def abstract_dynamic_kinetic_optical_pulse_grid_pattern_black_white_texture():
    """Tweak: A grid of pulsing rounded squares whose sizes pulse according to a 2D standing wave."""
    fig, ax = setup_ax()
    
    n_cols = 10
    n_rows = 10
    cell_size = 100 / n_cols
    
    for r in range(n_rows):
        for c in range(n_cols):
            cx = (c + 0.5) * cell_size
            cy = (r + 0.5) * cell_size
            
            # Dynamic pulse factor based on 2D wave
            pulse = 0.5 + 0.45 * (np.sin(c * 0.6) * np.cos(r * 0.6))
            w = cell_size * pulse
            
            if w <= 0.5:
                continue
                
            r_c = 0.25 * w
            box = FancyBboxPatch(
                (cx - w/2, cy - w/2),
                w,
                w,
                boxstyle=f"round,pad=0,rounding_size={r_c}",
                fill=False,
                edgecolor="black",
                linewidth=1.0,
            )
            ax.add_patch(box)

    save(fig, "abstract dynamic kinetic optical pulse grid pattern black white texture")


if __name__ == "__main__":
    abstract_dynamic_kinetic_optical_pulse_grid_pattern_black_white_texture()
