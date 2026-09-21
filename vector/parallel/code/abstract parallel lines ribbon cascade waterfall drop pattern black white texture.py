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


def abstract_parallel_lines_ribbon_cascade_waterfall_drop_pattern_black_white_texture():
    """Ribbon waterfall: horizontal lines flow normally then cascade downward in a central band"""
    fig, ax = setup_ax()

    n_lines = 75
    # Waterfall zone
    wx_left, wx_right = 35.0, 65.0
    fall_depth = 30.0   # how far lines drop in the cascade zone
    n_pts = 600

    for i in range(n_lines):
        y0 = -5 + i * (110.0 / (n_lines - 1))
        x = np.linspace(-5, 105, n_pts)
        y = np.zeros(n_pts)

        for j, xi in enumerate(x):
            if xi < wx_left:
                y[j] = y0
            elif xi > wx_right:
                y[j] = y0 - fall_depth
            else:
                # Smooth S-curve drop through the waterfall
                t = (xi - wx_left) / (wx_right - wx_left)  # 0..1
                s = t * t * (3 - 2 * t)   # smoothstep
                y[j] = y0 - fall_depth * s

        # Fade lineweight at the drop zone
        lw = 0.55
        ax.plot(x, y, color="black", linewidth=lw, solid_capstyle="round")

    # Draw subtle curtain lines in cascade zone
    for k in np.linspace(wx_left, wx_right, 10):
        ax.plot([k, k], [-6, 106], color="black", linewidth=0.18, alpha=0.25)

    save(fig, "abstract parallel lines ribbon cascade waterfall drop pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_ribbon_cascade_waterfall_drop_pattern_black_white_texture()
