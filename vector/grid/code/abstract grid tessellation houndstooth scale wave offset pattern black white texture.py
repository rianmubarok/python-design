import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
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


def draw():
    """Houndstooth tessellation with controlled scale wave distortion."""
    fig, ax = setup_ax()

    # Poligon Geometri Houndstooth Unit Presisi (8-point star / tooth unit)
    p0 = np.array([
        [0, 0], [1, 0], [1, 1], [2, 1], [2, 2], [1, 2],
        [1, 3], [0, 3], [0, 2], [-1, 2], [-1, 1], [0, 1]
    ], dtype=float) - np.array([0.5, 1.5])

    grid_size = 18
    step = 4.0

    center_offset = (grid_size - 1) * step / 2.0

    for row in range(grid_size):
        for col in range(grid_size):
            # Posisi kisi dasar
            base_x = col * step
            base_y = row * step

            # Gelombang skala yang terkontrol agar tidak menumpuk pekat
            s = 1.0 + 0.22 * np.sin(col * 0.4) * np.cos(row * 0.4)

            # Pergeseran posisi teratur
            shift_x = 0.35 * np.sin(row * 0.5)
            shift_y = 0.35 * np.cos(col * 0.5)

            cx = base_x + shift_x
            cy = base_y + shift_y

            # Poligon Hitam Utama
            ax.add_patch(
                Polygon(
                    p0 * s + [cx, cy],
                    closed=True,
                    facecolor="black",
                    edgecolor="black",
                    linewidth=0.5,
                    zorder=2,
                )
            )

    # Menyesuaikan tampilan agar simetris di tengah
    pad = 32.0
    ax.set_xlim(center_offset - pad, center_offset + pad)
    ax.set_ylim(center_offset - pad, center_offset + pad)

    save(
        fig,
        "abstract grid tessellation houndstooth scale wave offset pattern black white texture",
    )


if __name__ == "__main__":
    draw()