import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
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
    """Wild combo: Hermann grid + Ehrenstein — grid of circles with starburst lines at each intersection."""
    fig, ax = setup_ax()

    # Grid of circles
    n = 7
    spacing = 13.0
    disc_r = 4.5
    burst_len = 4.0
    n_burst = 8

    for r in range(n):
        for c in range(n):
            cx = (c - n / 2 + 0.5) * spacing
            cy = (r - n / 2 + 0.5) * spacing
            ax.add_patch(Circle((cx, cy), disc_r, facecolor="black"))

            # Starburst lines at intersection points (midway between circles)
            if c < n - 1:
                ix = cx + spacing / 2
                iy = cy
                for k in range(n_burst):
                    angle = k * np.pi / n_burst
                    dx = burst_len * np.cos(angle)
                    dy = burst_len * np.sin(angle)
                    ax.plot([ix - dx, ix + dx], [iy - dy, iy + dy],
                            color="black", linewidth=1.2)

            if r < n - 1:
                ix = cx
                iy = cy + spacing / 2
                for k in range(n_burst):
                    angle = k * np.pi / n_burst
                    dx = burst_len * np.cos(angle)
                    dy = burst_len * np.sin(angle)
                    ax.plot([ix - dx, ix + dx], [iy - dy, iy + dy],
                            color="black", linewidth=1.2)

    save(fig, "abstract optical hermann ehrenstein hybrid starburst grid pattern black white texture")


if __name__ == "__main__":
    generate()
