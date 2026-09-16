import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
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
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
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
    """Wild: Checkerboard that morphs from squares to circles from edge to center."""
    fig, ax = setup_ax()

    n = 24
    x_vals = np.linspace(-1.1, 1.1, n + 1)
    y_vals = np.linspace(-1.1, 1.1, n + 1)
    theta = np.linspace(0, 2 * np.pi, 40)

    for i in range(n):
        for j in range(n):
            if (i + j) % 2 != 0:
                continue

            cx = (x_vals[j] + x_vals[j + 1]) / 2
            cy = (y_vals[i] + y_vals[i + 1]) / 2
            half_w = (x_vals[j + 1] - x_vals[j]) / 2
            half_h = (y_vals[i + 1] - y_vals[i]) / 2

            # Morph factor: 0 at edges = square, 1 at center = circle
            dist = np.sqrt(cx**2 + cy**2)
            morph = max(0, 1.0 - dist / 1.0)

            if morph < 0.05:
                # Pure square
                pts = np.array([
                    [cx - half_w, cy - half_h],
                    [cx + half_w, cy - half_h],
                    [cx + half_w, cy + half_h],
                    [cx - half_w, cy + half_h],
                ])
            else:
                # Superellipse interpolation: square → circle
                p = 2.0 + 8.0 * (1 - morph)  # p=2 is circle, high p is square
                r_w = half_w * 0.95
                r_h = half_h * 0.95
                x_se = r_w * np.sign(np.cos(theta)) * np.abs(np.cos(theta))**(2 / p) + cx
                y_se = r_h * np.sign(np.sin(theta)) * np.abs(np.sin(theta))**(2 / p) + cy
                pts = np.column_stack([x_se, y_se])

            poly = Polygon(pts, closed=True, facecolor="black",
                           edgecolor="black", linewidth=0.2)
            ax.add_patch(poly)

    save(fig, "abstract optical checkerboard square circle morph gradient pattern black white texture")


if __name__ == "__main__":
    generate()
