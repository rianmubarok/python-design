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


def abstract_parallel_lines_accordion_fold_perspective_zigzag_pattern_black_white_texture():
    """Accordion paper fold: horizontal lines that zigzag in x, simulating folded paper perspective"""
    fig, ax = setup_ax()

    n_lines = 90
    n_folds = 8          # number of fold peaks across width
    fold_amp = 7.0       # max horizontal shift at peaks (perspective foreshortening)
    horizon_y = 50.0     # vanishing-point row (middle)

    xs_fold = np.linspace(0, 100, n_folds * 2 + 1)  # fold vertex x positions

    for i in range(n_lines):
        t = i / (n_lines - 1)            # 0 at bottom, 1 at top
        y_raw = t * 100.0

        # Perspective: lines near horizon are compressed vertically
        persp = 1 - 0.72 * np.exp(-((y_raw - horizon_y) ** 2) / 400)
        y = horizon_y + (y_raw - horizon_y) * persp

        # Fold shift amplitude grows near top & bottom, small near horizon
        dist_from_horizon = abs(y_raw - horizon_y) / 50.0
        amp = fold_amp * (0.3 + 0.7 * dist_from_horizon)

        # Build zigzag path
        x_pts = []
        y_pts = []
        for k, xv in enumerate(xs_fold):
            shift = amp if k % 2 == 0 else -amp
            x_pts.append(xv + shift)
            y_pts.append(y)

        lw = 0.3 + 0.55 * dist_from_horizon
        ax.plot(x_pts, y_pts, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines accordion fold perspective zigzag pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_accordion_fold_perspective_zigzag_pattern_black_white_texture()
