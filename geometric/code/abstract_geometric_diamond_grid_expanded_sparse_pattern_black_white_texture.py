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


def diamond_grid_expanded_sparse():
    """Teselasi belah ketupat dengan dimensi besar dan spasi lebar."""
    fig, ax = setup_ax()

    # Dimensi belah ketupat yang diperbesar
    w = 12.0  # 2x lebih lebar dari aslinya (6.0)
    h = 16.0  # 2x lebih tinggi dari aslinya (8.0)

    cols = 12  # Lebih sedikit kolom
    rows = 12  # Lebih sedikit baris

    # Jarak kisi yang lebih longgar
    step_x = w * 1.2  # 120% dari lebar untuk spasi ekstra
    step_y = h / 2.0 * 1.3  # 130% dari tinggi setengah untuk spasi vertikal ekstra

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

            # Garis yang lebih tebal untuk bentuk yang diperbesar
            lw = 2.0 if r % 2 == 0 else 1.5
            ax.plot(x_pts, y_pts, color="black", linewidth=lw, solid_capstyle="round")

            # Tambahkan titik pusat untuk aksen
            ax.plot(cx, cy, marker="o", markersize=1.5, color="black")

    # Framing simetris dengan padding lebih besar
    cx_final = (min_x + max_x) / 2.0
    cy_final = (min_y + max_y) / 2.0
    span_w = max_x - min_x
    span_h = max_y - min_y
    pad = max(span_w, span_h) / 2.0 + 5.0  # Padding lebih besar

    ax.set_xlim(cx_final - pad, cx_final + pad)
    ax.set_ylim(cy_final - pad, cy_final + pad)

    save(fig, "diamond grid expanded sparse")


if __name__ == "__main__":
    diamond_grid_expanded_sparse()