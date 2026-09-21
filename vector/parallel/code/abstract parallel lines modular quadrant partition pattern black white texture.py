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


def abstract_parallel_lines_modular_quadrant_partition_pattern_black_white_texture():
    """Garis paralel dalam partisi modular Bauhaus dengan orientasi dan skala berselang-seling"""
    fig, ax = setup_ax()

    # Definisi blok modular: [xmin, xmax, ymin, ymax, orientation ('H' atau 'V'), n_lines, lw]
    blocks = [
        # Kuadran Kiri Bawah (Blok besar horizontal)
        (-5, 45, -5, 45, "H", 24, 1.8),
        # Kuadran Kanan Bawah (Blok vertikal rapat)
        (45, 105, -5, 45, "V", 32, 1.2),
        # Kuadran Kiri Atas (Blok vertikal tebal)
        (-5, 45, 45, 105, "V", 18, 2.5),
        # Sub-blok Kanan Atas 1 (Horizontal rapat)
        (45, 105, 45, 78, "H", 20, 1.4),
        # Sub-blok Kanan Atas 2 (Vertikal mikro)
        (45, 75, 78, 105, "V", 16, 1.6),
        # Sub-blok Kanan Atas 3 (Horizontal berirama)
        (75, 105, 78, 105, "H", 14, 2.2),
    ]

    for xmin, xmax, ymin, ymax, ori, count, lw in blocks:
        # Garis batas pembagi blok
        rect_border = plt.Rectangle(
            (xmin, ymin), xmax - xmin, ymax - ymin,
            fill=False, edgecolor="black", linewidth=2.4, joinstyle="miter"
        )
        ax.add_patch(rect_border)

        # Garis paralel dalam blok dengan margin kecil
        pad = 1.2
        if ori == "H":
            y_coords = np.linspace(ymin + pad, ymax - pad, count)
            for y in y_coords:
                ax.plot([xmin + pad, xmax - pad], [y, y], color="black", linewidth=lw, solid_capstyle="butt")
        else:
            x_coords = np.linspace(xmin + pad, xmax - pad, count)
            for x in x_coords:
                ax.plot([x, x], [ymin + pad, ymax - pad], color="black", linewidth=lw, solid_capstyle="butt")

    save(fig, "abstract parallel lines modular quadrant partition pattern black white texture")


if __name__ == "__main__":
    abstract_parallel_lines_modular_quadrant_partition_pattern_black_white_texture()
