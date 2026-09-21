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
    """Curved Café Wall Illusion: Continuous rows of alternating black and white tiles separated by gray mortar lines."""
    fig, ax = setup_ax()

    n_rows = 26
    tile_w = 4.5
    tile_h = 3.8
    mortar_lw = 1.5

    # Pola pergeseran khas Cafe Wall (0, 0.5, 1.0, 0.5)
    shifts = [0.0, 0.5, 1.0, 0.5]

    for row in range(n_rows):
        row_y = -48 + row * tile_h
        shift_val = shifts[row % 4] * tile_w
        curvature = 0.0025 * (row - n_rows / 2)

        # 1. Isian Bata Rapat Hitam dan Putih Berselang-seling
        n_cols = 35
        for col in range(-n_cols, n_cols):
            x1 = col * tile_w + shift_val
            x2 = x1 + tile_w

            if x2 < -55 or x1 > 55:
                continue

            # Sampel kurva di sepanjang lebar bata agar sisi lengkungnya mulus
            x_samples = np.linspace(x1, x2, 15)
            y_bottom = row_y + curvature * (x_samples**2)
            y_top = (row_y + tile_h) + curvature * (x_samples**2)

            # Gabungkan titik-titik polygon (bawah dari kiri->kanan, atas dari kanan->kiri)
            pts_bottom = np.column_stack([x_samples, y_bottom])
            pts_top = np.column_stack([x_samples[::-1], y_top[::-1]])
            pts = np.vstack([pts_bottom, pts_top])

            color = "black" if (col % 2 == 0) else "white"

            poly = Polygon(pts, closed=True, facecolor=color, edgecolor="none", zorder=1)
            ax.add_patch(poly)

        # 2. Garis Pembatas (Mortar Line) Abu-Abu Rapi di Setiap Sisi Baris
        x_mortar = np.linspace(-55, 55, 300)
        y_mortar = row_y + curvature * (x_mortar**2)
        ax.plot(x_mortar, y_mortar, color="gray", linewidth=mortar_lw, zorder=3)

    save(fig, "abstract optical cafe wall illusion curved arc row pattern black white texture")


if __name__ == "__main__":
    generate()