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


def abstract_parallel_lines_concentric_rounded_rect_dynamic_squash_pattern_black_white_texture():
    """Tweak: Concentric rounded rects where aspect ratio squashes vertically then horizontally."""
    fig, ax = setup_ax()
    n_rects = 40
    for i in range(n_rects):
        # Base size
        base_size = 100 - i * 2.4
        if base_size <= 2:
            break
            
        # Dynamic squashing
        phase = (i / n_rects) * 3 * np.pi
        squash_x = 1.0 - 0.3 * max(0, np.sin(phase))
        squash_y = 1.0 - 0.3 * max(0, -np.sin(phase))
        
        w = base_size * squash_x
        h = base_size * squash_y
        
        x_pos = 50 - w / 2
        y_pos = 50 - h / 2
        
        r = 0.2 * min(w, h)
        lw = 0.5 + 0.3 * (1 - i / n_rects)
        
        box = FancyBboxPatch(
            (x_pos, y_pos),
            w,
            h,
            boxstyle=f"round,pad=0,rounding_size={r}",
            fill=False,
            edgecolor="black",
            linewidth=lw,
        )
        ax.add_patch(box)
        
    save(fig, "abstract parallel lines concentric rounded rect dynamic squash pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_concentric_rounded_rect_dynamic_squash_pattern_black_white_texture()
