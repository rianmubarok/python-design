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
    """Muller-Lyer with curved/arc chevrons instead of straight-line arrows."""
    fig, ax = setup_ax()

    line_len = 14.0
    half_len = line_len / 2.0
    arrow_size = 3.5

    rows = np.linspace(-42, 42, 10)
    cols = np.linspace(-36, 36, 6)
    t_arc = np.linspace(-1, 1, 30)

    for i, y in enumerate(rows):
        for j, x_center in enumerate(cols):
            x1 = x_center - half_len
            x2 = x_center + half_len
            ax.plot([x1, x2], [y, y], color="black", linewidth=2.2)

            inward = (i + j) % 2 == 0
            dir1 = 1 if inward else -1
            dir2 = -1 if inward else 1

            # Curved chevron at left end
            for sign in [1, -1]:
                cx = x1 + dir1 * arrow_size * np.abs(t_arc)
                cy = y + sign * arrow_size * t_arc + sign * 0.8 * t_arc**2
                ax.plot(cx, cy, color="black", linewidth=1.8)

            # Curved chevron at right end
            for sign in [1, -1]:
                cx = x2 + dir2 * arrow_size * np.abs(t_arc)
                cy = y + sign * arrow_size * t_arc + sign * 0.8 * t_arc**2
                ax.plot(cx, cy, color="black", linewidth=1.8)

    save(fig, "abstract optical muller lyer curved arc chevron pattern black white texture")


if __name__ == "__main__":
    generate()
