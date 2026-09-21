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
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
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


def generate():
    """Wild: Pinwheel spokes that swell their linewidth according to a sine envelope — 'breathing' spokes."""
    fig, ax = setup_ax()

    n_spokes = 80
    n_pts = 300
    t = np.linspace(0, 45, n_pts)

    for i in range(n_spokes):
        base_angle = i * 2 * np.pi / n_spokes
        angle = base_angle + 0.05 * t

        x = t * np.cos(angle)
        y = t * np.sin(angle)

        # Linewidth modulated by sine along length
        # Plot segment-by-segment to simulate variable linewidth
        envelope = 0.3 + 2.2 * (np.sin(t * 0.18 + i * 0.4))**2
        for seg in range(0, n_pts - 1, 3):
            lw_seg = float(envelope[seg])
            ax.plot(x[seg:seg+4], y[seg:seg+4], color="black", linewidth=lw_seg, solid_capstyle='round')

    save(fig, "abstract optical pinwheel breathing variable width spoke pattern black white texture")


if __name__ == "__main__":
    generate()
