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
    """Muller-Lyer arranged radially — segments emanate outward from center with alternating chevrons."""
    fig, ax = setup_ax()

    n_rays = 24
    line_len = 16.0
    arrow_size = 3.0
    inner_r = 6.0

    for i in range(n_rays):
        angle = i * 2 * np.pi / n_rays

        # Segment along the ray
        x1 = inner_r * np.cos(angle)
        y1 = inner_r * np.sin(angle)
        x2 = (inner_r + line_len) * np.cos(angle)
        y2 = (inner_r + line_len) * np.sin(angle)
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=2.2)

        # Perpendicular direction for chevrons
        perp_angle = angle + np.pi / 2
        px = np.cos(perp_angle)
        py = np.sin(perp_angle)

        inward = i % 2 == 0
        dir1 = 1 if inward else -1
        dir2 = -1 if inward else 1

        # Inner end chevrons
        ax.plot([x1 + dir1 * arrow_size * np.cos(angle) + arrow_size * px,
                 x1,
                 x1 + dir1 * arrow_size * np.cos(angle) - arrow_size * px],
                [y1 + dir1 * arrow_size * np.sin(angle) + arrow_size * py,
                 y1,
                 y1 + dir1 * arrow_size * np.sin(angle) - arrow_size * py],
                color="black", linewidth=1.8)

        # Outer end chevrons
        ax.plot([x2 + dir2 * arrow_size * np.cos(angle) + arrow_size * px,
                 x2,
                 x2 + dir2 * arrow_size * np.cos(angle) - arrow_size * px],
                [y2 + dir2 * arrow_size * np.sin(angle) + arrow_size * py,
                 y2,
                 y2 + dir2 * arrow_size * np.sin(angle) - arrow_size * py],
                color="black", linewidth=1.8)

    save(fig, "abstract optical muller lyer radial spoke starburst pattern black white texture")


if __name__ == "__main__":
    generate()
