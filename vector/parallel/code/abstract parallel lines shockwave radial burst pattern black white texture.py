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


def abstract_parallel_lines_shockwave_radial_burst_pattern_black_white_texture():
    """Wild: concentric shockwave rings combined with radial spokes — explosion cross-section"""
    fig, ax = setup_ax()
    cx, cy = 50.0, 50.0

    # --- Concentric shockwave rings (non-uniform, compressed near centre) ---
    n_rings = 28
    for k in range(n_rings):
        # spacing compressed near core, expanding outward (shockwave)
        r = 3.5 + (k ** 1.35) * 2.1
        if r > 72:
            break
        # Ring thickness pulses with alternate thick/thin
        lw = 1.8 if k % 3 == 0 else 0.55
        theta = np.linspace(0, 2 * np.pi, 600)
        # Deform circle slightly: slight ellipse + radial ripple
        ripple = 1 + 0.04 * np.cos(8 * theta + k * 0.7)
        xr = cx + r * ripple * np.cos(theta)
        yr = cy + r * ripple * np.sin(theta)
        ax.plot(xr, yr, color="black", linewidth=lw, solid_capstyle="round")

    # --- Radial spokes fanning outward ---
    n_spokes = 24
    for j in range(n_spokes):
        angle = j * 2 * np.pi / n_spokes
        # Spokes start at r=4, end at r=70, with slight wobble
        r_vals = np.linspace(4, 70, 300)
        wobble = 0.8 * np.sin(r_vals * 0.25 + j * 1.1)
        xs = cx + r_vals * np.cos(angle + np.deg2rad(wobble))
        ys = cy + r_vals * np.sin(angle + np.deg2rad(wobble))
        ax.plot(xs, ys, color="black", linewidth=0.45, alpha=0.7, solid_capstyle="round")

    save(fig, "abstract parallel lines shockwave radial burst pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_shockwave_radial_burst_pattern_black_white_texture()
