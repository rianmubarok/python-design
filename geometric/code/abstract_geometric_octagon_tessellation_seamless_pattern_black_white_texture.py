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


def draw_octagon(cx, cy, r):
    """Menggambar oktagon beraturan dengan jari-jari luar r."""
    angles = np.linspace(np.pi / 8, 2 * np.pi + np.pi / 8, 9)
    x = cx + r * np.cos(angles)
    y = cy + r * np.sin(angles)
    return x, y


def draw_square(cx, cy, side):
    """Menggambar persegi sejajar sumbu dengan panjang sisi side."""
    h = side / 2.0
    x = [cx - h, cx + h, cx + h, cx - h, cx - h]
    y = [cy - h, cy - h, cy + h, cy + h, cy - h]
    return x, y


def octagon_tessellation_seamless():
    """Teselasi presisi segi delapan dan persegi yang saling mengunci (Truncated Square Tiling)."""
    fig, ax = setup_ax()

    # Panjang sisi bersama antara oktagon dan persegi
    s = 6.0
    # Jarak antar-pusat oktagon yang presisi
    D = s * (1.0 + np.sqrt(2.0))
    # Jari-jari luar oktagon
    r_oct = s / (2.0 * np.sin(np.pi / 8.0))

    cols, rows = 8, 8

    # Perhitungan offset untuk memposisikan teselasi simetris di tengah kanvas (50, 50)
    total_w = (cols - 1) * D
    total_h = (rows - 1) * D
    offset_x = 50.0 - total_w / 2.0
    offset_y = 50.0 - total_h / 2.0

    # 1. Gambar Oktagon pada setiap simpul kisi
    for r in range(rows):
        for c in range(cols):
            cx = offset_x + c * D
            cy = offset_y + r * D

            x_oct, y_oct = draw_octagon(cx, cy, r_oct)
            ax.plot(
                x_oct,
                y_oct,
                color="black",
                linewidth=1.2,
                solid_capstyle="round",
                zorder=2,
            )

    # 2. Gambar Persegi pada persimpangan antar-oktagon
    for r in range(rows - 1):
        for c in range(cols - 1):
            sq_cx = offset_x + c * D + D / 2.0
            sq_cy = offset_y + r * D + D / 2.0

            x_sq, y_sq = draw_square(sq_cx, sq_cy, s)
            ax.plot(
                x_sq,
                y_sq,
                color="black",
                linewidth=1.2,
                solid_capstyle="round",
                zorder=2,
            )

    # Framing simetris terpusat penuh
    pad = (total_w / 2.0) + r_oct + 2.0
    ax.set_xlim(50.0 - pad, 50.0 + pad)
    ax.set_ylim(50.0 - pad, 50.0 + pad)

    save(fig, "octagon tessellation seamless")


if __name__ == "__main__":
    octagon_tessellation_seamless()