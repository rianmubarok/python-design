import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
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


def draw():
    """Triangular lattice with mini Lissajous orbits at every vertex node."""
    fig, ax = setup_ax()

    a = 10.0
    h = a * np.sqrt(3) / 2.0
    t = np.linspace(0, 2 * np.pi, 120)

    rows, cols = 20, 20  # Sedikit lebih besar untuk menghindari tepi terpotong
    center_x = (cols - 1) * a / 2.0
    center_y = (rows - 1) * h / 2.0

    lw_grid = 0.5
    lw_liss = 1.2

    # 1. Plot Jaringan Kisi Segitiga yang Konsisten
    for r in range(rows):
        # Garis Horizontal (digambar hanya sekali per baris)
        # Menghubungkan titik paling kiri dan paling kanan di baris r
        start_x = 0.0 + (a / 2.0 if r % 2 else 0.0)
        end_x = (cols - 1) * a + (a / 2.0 if r % 2 else 0.0)
        start_y = end_y = r * h
        ax.plot([start_x, end_x], [start_y, end_y], color="black", linewidth=lw_grid, zorder=1)

        # Garis Diagonal
        for c in range(cols):
            cx = c * a + (a / 2.0 if r % 2 else 0.0)
            cy = r * h

            # Hanya menggambar garis diagonal 'ke atas'
            if r < rows - 1:
                # Diagonal Kanan
                ax.plot([cx, cx + a / 2.0], [cy, cy + h], color="black", linewidth=lw_grid, zorder=1)
                # Diagonal Kiri
                ax.plot([cx, cx - a / 2.0], [cy, cy + h], color="black", linewidth=lw_grid, zorder=1)

    # 2. Plot Orbit Lissajous di Setiap Simpul Persimpangan
    for r in range(rows):
        for c in range(cols):
            cx = c * a + (a / 2.0 if r % 2 else 0.0)
            cy = r * h

            # Menghitung amplitudo dan frekuensi untuk variasi visual
            amp = 1.6 + 0.9 * (0.5 + 0.5 * np.sin(c * 0.5 + r * 0.4))
            fx, fy = 2 + (c % 2), 3 + (r % 2)

            xs = cx + amp * np.sin(fx * t)
            ys = cy + amp * np.sin(fy * t + np.pi / 4.0)

            # Memplot Lissajous (tanpa memplot kisi lagi)
            ax.plot(xs, ys, color="black", linewidth=lw_liss, zorder=2)

    # Menentukan jendela tampilan simetris tepat di tengah
    pad = 36.0
    ax.set_xlim(center_x - pad, center_x + pad)
    ax.set_ylim(center_y - pad, center_y + pad)

    save(
        fig,
        "abstract grid tessellation triangular node lissajous orbit pattern black white texture",
    )


if __name__ == "__main__":
    draw()