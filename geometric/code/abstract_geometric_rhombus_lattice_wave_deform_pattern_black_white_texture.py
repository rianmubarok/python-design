from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.use("Agg")

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


def rhombus_lattice_wave_deform():
    """Rhombus lattice pattern with seamless continuous sinusoidal wave deformation."""
    fig, ax = setup_ax()

    # Parameter grid dasar
    rows, cols = 28, 28
    step_x = 6.0
    step_y = 5.0

    # 1. Buat matriks koordinat simpul (grid vertices)
    grid_x = np.zeros((rows, cols))
    grid_y = np.zeros((rows, cols))

    # Hitung posisi dasar dengan pergeseran selang-seling (staggered)
    for r in range(rows):
        for c in range(cols):
            bx = c * step_x
            if r % 2 != 0:
                bx += step_x * 0.5
            by = r * step_y

            # 2. Terapkan deformasi gelombang global pada titik simpul
            wave_x = 2.2 * np.sin(0.2 * by + 0.1 * bx)
            wave_y = 1.8 * np.cos(0.25 * bx)

            grid_x[r, c] = bx + wave_x
            grid_y[r, c] = by + wave_y

    # Pusatkan grid ke titik (50, 50)
    center_x = (grid_x.min() + grid_x.max()) / 2.0
    center_y = (grid_y.min() + grid_y.max()) / 2.0
    grid_x += 50.0 - center_x
    grid_y += 50.0 - center_y

    # 3. Hubungkan titik simpul untuk membentuk belah ketupat tersambung (Interlocking)
    for r in range(rows - 1):
        for c in range(cols - 1):
            if r % 2 == 0:
                # Belah ketupat tipe A
                p1 = (grid_x[r, c], grid_y[r, c])
                p2 = (grid_x[r, c + 1], grid_y[r, c + 1])
                p3 = (grid_x[r + 1, c], grid_y[r + 1, c])
                p4 = (grid_x[r + 1, c - 1], grid_y[r + 1, c - 1]) if c > 0 else None
            else:
                # Belah ketupat tipe B
                p1 = (grid_x[r, c], grid_y[r, c])
                p2 = (grid_x[r, c + 1], grid_y[r, c + 1])
                p3 = (grid_x[r + 1, c + 1], grid_y[r + 1, c + 1])
                p4 = (grid_x[r + 1, c], grid_y[r + 1, c])

            # Gambar garis tepi belah ketupat
            if r % 2 == 0:
                poly_x = [grid_x[r, c], grid_x[r, c + 1], grid_x[r + 1, c + 1], grid_x[r + 1, c], grid_x[r, c]]
                poly_y = [grid_y[r, c], grid_y[r, c + 1], grid_y[r + 1, c + 1], grid_y[r + 1, c], grid_y[r, c]]
            else:
                poly_x = [grid_x[r, c], grid_x[r, c + 1], grid_x[r + 1, c + 1], grid_x[r + 1, c], grid_x[r, c]]
                poly_y = [grid_y[r, c], grid_y[r, c + 1], grid_y[r + 1, c + 1], grid_y[r + 1, c], grid_y[r, c]]

            ax.plot(poly_x, poly_y, color="black", linewidth=0.8, solid_capstyle="round")

    # Framing simetris
    pad = 42.0
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)

    save(fig, "rhombus lattice wave deform")


if __name__ == "__main__":
    rhombus_lattice_wave_deform()