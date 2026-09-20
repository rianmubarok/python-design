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


def draw_diamond(cx, cy, w, h):
    """Menggambar belah ketupat (diamond) berpusat di (cx, cy)."""
    x = [cx, cx + w / 2.0, cx, cx - w / 2.0, cx]
    y = [cy + h / 2.0, cy, cy - h / 2.0, cy, cy + h / 2.0]
    return x, y


def diamond_grid_compressed_density():
    """Teselasi belah ketupat dengan kepadatan tinggi dan dimensi terkompresi."""
    fig, ax = setup_ax()

    # Dimensi belah ketupat yang lebih kecil untuk kepadatan tinggi
    w = 4.0  # Lebih sempit dari aslinya (6.0)
    h = 5.0  # Lebih pendek dari aslinya (8.0)

    cols = 30  # Lebih banyak kolom
    rows = 30  # Lebih banyak baris

    # Jarak kisi yang lebih rapat
    step_x = w * 0.9  # 90% dari lebar untuk tumpang tindih minimal
    step_y = h / 2.0 * 0.85  # 85% dari tinggi setengah untuk kompresi vertikal

    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")

    for r in range(rows):
        for c in range(cols):
            cx = c * step_x
            if r % 2 != 0:
                cx += step_x / 2.0
            cy = r * step_y

            x_pts, y_pts = draw_diamond(cx, cy, w, h)

            min_x, max_x = min(min_x, min(x_pts)), max(max_x, max(x_pts))
            min_y, max_y = min(min_y, min(y_pts)), max(max_y, max(y_pts))

            # Variasi ketebalan garis yang lebih halus untuk kepadatan tinggi
            lw = 0.6 + 0.2 * (r % 3)  # Variasi subtil berdasarkan modulo 3
            ax.plot(x_pts, y_pts, color="black", linewidth=lw, solid_capstyle="round")

    # Framing simetris dengan padding yang lebih ketat
    cx_final = (min_x + max_x) / 2.0
    cy_final = (min_y + max_y) / 2.0
    span_w = max_x - min_x
    span_h = max_y - min_y
    pad = max(span_w, span_h) / 2.0 + 1.0  # Padding minimal

    ax.set_xlim(cx_final - pad, cx_final + pad)
    ax.set_ylim(cy_final - pad, cy_final + pad)

    save(fig, "diamond grid compressed density")


if __name__ == "__main__":
    diamond_grid_compressed_density()