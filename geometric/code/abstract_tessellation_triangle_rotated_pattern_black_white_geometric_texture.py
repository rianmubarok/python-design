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
    jpg_path = JPG_DIR / f"{name}_{DATE}.jpg"
    svg_path = SVG_DIR / f"{name}_{DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def tessellation_triangle_rotated():
    """Tweak: the whole triangular tessellation is resized and tilted off-axis"""
    fig, ax = setup_ax()
    size = 8.0
    h = size * np.sqrt(3) / 2
    rad = np.radians(28.0)
    ca, sa = np.cos(rad), np.sin(rad)

    def rot(px, py):
        dx, dy = px - 50.0, py - 50.0
        return 50.0 + dx * ca - dy * sa, 50.0 + dx * sa + dy * ca

    for row in range(-4, 18):
        for col in range(-4, 18):
            x = col * size + (row % 2) * size / 2
            y = row * h
            if (row + col) % 2 == 0:
                tri = [(x, y), (x + size, y), (x + size / 2, y + h)]
            else:
                tri = [(x, y + h), (x + size, y + h), (x + size / 2, y)]
            pts = [rot(px, py) for px, py in tri]
            xs = [p[0] for p in pts] + [pts[0][0]]
            ys = [p[1] for p in pts] + [pts[0][1]]
            ax.plot(xs, ys, color="black", linewidth=0.8)
    save(fig, "abstract_tessellation_triangle_rotated_pattern_black_white_geometric_texture")


if __name__ == "__main__":
    tessellation_triangle_rotated()
