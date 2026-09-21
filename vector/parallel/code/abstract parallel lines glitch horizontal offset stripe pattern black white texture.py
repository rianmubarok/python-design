import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 7
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


def abstract_parallel_lines_glitch_horizontal_offset_stripe_pattern_black_white_texture():
    """Digital glitch: horizontal lines broken into segments with random horizontal offsets (like corrupted video)"""
    fig, ax = setup_ax()

    n_lines = 100
    n_segments = 18        # segments per line
    seg_width = 110.0 / n_segments
    max_glitch = 9.0       # max pixel offset per segment
    glitch_prob = 0.22     # chance any segment is glitched
    thick_prob = 0.08      # chance a line is extra thick (error block)

    for i in range(n_lines):
        y = -5 + i * (110.0 / (n_lines - 1))
        is_thick = np.random.rand() < thick_prob
        base_lw = 2.2 if is_thick else 0.5

        for k in range(n_segments):
            x0 = -5 + k * seg_width
            x1 = x0 + seg_width

            glitched = np.random.rand() < glitch_prob
            offset = np.random.uniform(-max_glitch, max_glitch) if glitched else 0.0
            segment_lw = base_lw * np.random.uniform(0.5, 2.5) if glitched else base_lw

            ax.plot([x0, x1], [y + offset, y + offset],
                    color="black", linewidth=segment_lw,
                    solid_capstyle="butt")

    save(fig, "abstract parallel lines glitch horizontal offset stripe pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_glitch_horizontal_offset_stripe_pattern_black_white_texture()
