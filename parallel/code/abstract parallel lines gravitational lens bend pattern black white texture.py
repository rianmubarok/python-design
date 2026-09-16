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


def abstract_parallel_lines_gravitational_lens_bend_pattern_black_white_texture():
    """Wild: horizontal lines bent as if passing around a massive gravitational lens"""
    fig, ax = setup_ax()
    cx, cy = 50.0, 50.0
    # Einstein ring radius in canvas units
    R_E = 18.0
    n_lines = 70
    x = np.linspace(-5, 105, 900)

    for i in range(n_lines):
        y0 = -5 + i * (110 / (n_lines - 1))
        y = np.zeros_like(x)
        for j, xi in enumerate(x):
            dx = xi - cx
            dy = y0 - cy
            r2 = dx * dx + dy * dy
            if r2 < 0.01:
                y[j] = np.nan
                continue
            # Deflection angle: alpha = R_E^2 / r  pointing toward centre
            alpha = R_E ** 2 / r2
            # Deflect the y coordinate proportionally
            y[j] = y0 + alpha * (cy - y0) / np.sqrt(r2)
        # Clip to canvas
        mask = (y < -6) | (y > 106)
        y = np.where(mask, np.nan, y)
        dist_to_cx = abs(y0 - cy) / 55
        lw = 0.45 + 0.8 * (1 - dist_to_cx ** 0.7)
        ax.plot(x, y, color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines gravitational lens bend pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_gravitational_lens_bend_pattern_black_white_texture()
