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


def abstract_dynamic_wave_distortion_concentric_rounded_rect_pattern_black_white_texture():
    """Tweak: Concentric rounded rects undergoing a dynamic wave ripple distortion field."""
    fig, ax = setup_ax()
    
    n_rects = 35
    for i in range(n_rects):
        margin = i * 1.4
        w = 100 - 2 * margin
        if w <= 2:
            break
            
        r = 0.25 * w
        lw = 0.5 + 0.4 * (1 - i / n_rects)
        
        # Dynamic wave ripple offset
        ripple_x = 3.0 * np.sin(i * 0.4)
        ripple_y = 3.0 * np.cos(i * 0.4)
        
        box = FancyBboxPatch(
            (margin + ripple_x, margin + ripple_y),
            w,
            w,
            boxstyle=f"round,pad=0,rounding_size={r}",
            fill=False,
            edgecolor="black",
            linewidth=lw,
        )
        ax.add_patch(box)

    save(fig, "abstract dynamic wave distortion concentric rounded rect pattern black white texture")


if __name__ == "__main__":
    abstract_dynamic_wave_distortion_concentric_rounded_rect_pattern_black_white_texture()
