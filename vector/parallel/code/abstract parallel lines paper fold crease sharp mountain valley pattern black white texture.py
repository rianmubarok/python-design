import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


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
    print(f"Saved: {jpg_path} | {svg_path}")


def abstract_parallel_lines_paper_fold_crease_sharp_mountain_valley_pattern_black_white_texture():
    """
    Horizontal parallel lines that are sharply folded at multiple vertical crease
    positions — alternating mountain/valley folds like origami or fan folding.
    Each fold displaces the y-coordinate by a sharp V-shaped offset, creating
    the illusion of pleated paper with crisp creases and angled facets.
    """
    fig, ax = setup_ax()

    n_lines = 80
    x = np.linspace(-5, 105, 1000)

    # Crease positions (x-values) — slightly irregular for interest
    crease_xs = [18, 32, 50, 65, 80]
    fold_amplitudes = [10, -8, 12, -9, 7]   # mountain (+) or valley (-)
    fold_sharpness = 1.2   # controls how sharp the V is (lower = sharper)

    y_positions = np.linspace(-5, 105, n_lines)

    for y0 in y_positions:
        y = np.full_like(x, y0, dtype=float)

        # Accumulate V-fold offsets from each crease
        for cx, amp in zip(crease_xs, fold_amplitudes):
            # Signed distance from crease
            d = x - cx
            # Soft-V shape using tanh to round the crease tip slightly
            fold_offset = amp * (1 - np.exp(-np.abs(d) / fold_sharpness)) * np.sign(d)
            # But we want the V: fold bends the paper away from the crease
            # Paper folds: both sides tilt toward each other (mountain) or away (valley)
            fold_y = -np.abs(d / (fold_sharpness * 2.5)) * amp / max(abs(amp), 1)
            # Sharp V: |d| scaled
            sharp_v = np.abs(d) * (abs(amp) / 55.0)
            y = y + np.sign(amp) * sharp_v * np.exp(-np.abs(d) / 30.0)

        # Mask out-of-canvas
        mask = (y < -6) | (y > 106)
        y = np.where(mask, np.nan, y)

        lw = 0.5
        ax.plot(x, y, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines paper fold crease sharp mountain valley pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_paper_fold_crease_sharp_mountain_valley_pattern_black_white_texture()
