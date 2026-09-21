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
    """Wild: Moire from concentric SQUARES (not circles) — two sets offset and slightly rotated."""
    fig, ax = setup_ax()
    from matplotlib.patches import Polygon

    def draw_concentric_squares(ax, cx, cy, angle_offset, n, max_size, lw):
        for i in range(n):
            s = max_size * (1 - i / n)
            if s <= 0.5:
                break
            pts = np.array([[-s, -s], [s, -s], [s, s], [-s, s]])
            rot = np.array([
                [np.cos(angle_offset), -np.sin(angle_offset)],
                [np.sin(angle_offset), np.cos(angle_offset)]
            ])
            pts = pts @ rot.T
            pts[:, 0] += cx
            pts[:, 1] += cy
            poly = Polygon(pts, closed=True, fill=False,
                           edgecolor="black", linewidth=lw)
            ax.add_patch(poly)

    draw_concentric_squares(ax, -2, -2, 0, 80, 60, 0.9)
    draw_concentric_squares(ax, 2, 2, np.radians(3), 80, 60, 0.9)

    save(fig, "abstract optical moire concentric squares dual rotation offset pattern black white texture")


if __name__ == "__main__":
    generate()
