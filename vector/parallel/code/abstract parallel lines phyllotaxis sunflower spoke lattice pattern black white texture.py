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


def abstract_parallel_lines_phyllotaxis_sunflower_spoke_lattice_pattern_black_white_texture():
    """Phyllotaxis: short tangent line segments placed at golden-angle spiral positions"""
    fig, ax = setup_ax()

    golden_angle = np.pi * (3 - np.sqrt(5))   # ~137.5 degrees in radians
    n_points = 1800
    cx, cy = 50.0, 50.0
    scale = 2.05    # controls overall radius
    seg_len = 2.8   # length of each tangent segment

    for k in range(n_points):
        r = scale * np.sqrt(k + 1)
        theta = k * golden_angle
        x = cx + r * np.cos(theta)
        y = cy + r * np.sin(theta)

        if x < -5 or x > 105 or y < -5 or y > 105:
            continue

        # Draw short segment tangent to the spiral direction
        tang_angle = theta + np.pi / 2
        dx = 0.5 * seg_len * np.cos(tang_angle)
        dy = 0.5 * seg_len * np.sin(tang_angle)

        # Linewidth scales with radius (outer ones thinner)
        lw = 0.65 - 0.38 * (r / (scale * np.sqrt(n_points)))
        lw = max(lw, 0.18)
        ax.plot([x - dx, x + dx], [y - dy, y + dy],
                color="black", linewidth=lw, solid_capstyle="round")

    save(fig, "abstract parallel lines phyllotaxis sunflower spoke lattice pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_phyllotaxis_sunflower_spoke_lattice_pattern_black_white_texture()
