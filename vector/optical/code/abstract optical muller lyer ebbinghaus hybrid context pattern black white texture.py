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
    """Wild: Muller-Lyer meets Ebbinghaus — chevron arrows + surrounding context circles combined."""
    fig, ax = setup_ax()
    from matplotlib.patches import Circle

    line_len = 12.0
    half_len = line_len / 2.0
    arrow_size = 2.8

    rows = np.linspace(-40, 40, 8)
    cols = np.linspace(-34, 34, 5)

    for i, y in enumerate(rows):
        for j, x_center in enumerate(cols):
            x1 = x_center - half_len
            x2 = x_center + half_len
            ax.plot([x1, x2], [y, y], color="black", linewidth=2.0)

            inward = (i + j) % 2 == 0
            dir1 = 1 if inward else -1
            dir2 = -1 if inward else 1

            # Chevrons
            ax.plot([x1 + dir1 * arrow_size, x1, x1 + dir1 * arrow_size],
                    [y + arrow_size, y, y - arrow_size], color="black", linewidth=1.6)
            ax.plot([x2 + dir2 * arrow_size, x2, x2 + dir2 * arrow_size],
                    [y + arrow_size, y, y - arrow_size], color="black", linewidth=1.6)

            # Ebbinghaus context circles at each endpoint
            if inward:
                for end_x in [x1, x2]:
                    for k in range(4):
                        a = k * np.pi / 2
                        ox = end_x + 2.5 * np.cos(a)
                        oy = y + 2.5 * np.sin(a)
                        ax.add_patch(Circle((ox, oy), 0.8, fill=False,
                                            edgecolor="black", linewidth=1.0))
            else:
                for end_x in [x1, x2]:
                    for k in range(3):
                        a = k * 2 * np.pi / 3
                        ox = end_x + 4.0 * np.cos(a)
                        oy = y + 4.0 * np.sin(a)
                        ax.add_patch(Circle((ox, oy), 2.0, fill=False,
                                            edgecolor="black", linewidth=1.0))

    save(fig, "abstract optical muller lyer ebbinghaus hybrid context pattern black white texture")


if __name__ == "__main__":
    generate()
