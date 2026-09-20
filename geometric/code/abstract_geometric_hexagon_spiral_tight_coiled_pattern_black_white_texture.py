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


def draw_hexagon(cx, cy, size, rotation=0.0):
    """Menggambar heksagon beraturan presisi."""
    angles = np.linspace(0, 2 * np.pi, 7) + rotation
    x = cx + size * np.cos(angles)
    y = cy + size * np.sin(angles)
    return x, y


def hexagon_spiral_tight_coiled():
    """Heksagon spiral dengan belitan rapat dan dimensi terkompresi."""
    fig, ax = setup_ax()

    cx, cy = 50.0, 50.0
    n_hexagons = 120  # Lebih banyak heksagon
    spiral_turns = 6.5  # Lebih banyak belitan

    min_x, max_x = cx, cx
    min_y, max_y = cy, cy

    for i in range(n_hexagons):
        t = i / n_hexagons
        angle = t * spiral_turns * 2 * np.pi
        
        # Radius yang lebih rapat dengan eksponen lebih tinggi
        radius = 0.8 + 25.0 * (t ** 1.4)  # Fungsi eksponen lebih curam

        hex_x = cx + radius * np.cos(angle)
        hex_y = cy + radius * np.sin(angle)

        # Ukuran heksagon lebih kecil dan bertambah lebih cepat
        hex_size = 0.6 + 3.0 * (t ** 1.3)  # Pertumbuhan lebih cepat

        # Rotasi (twist) yang lebih intens
        twist = angle * 1.2 + t * np.pi * 1.5

        x_hex, y_hex = draw_hexagon(hex_x, hex_y, hex_size, rotation=twist)

        # Melacak area bounding box untuk framing
        min_x, max_x = min(min_x, x_hex.min()), max(max_x, x_hex.max())
        min_y, max_y = min(min_y, y_hex.min()), max(max_y, y_hex.max())

        # Ketebalan garis lebih tipis untuk kepadatan tinggi
        lw = max(0.3, 1.5 - 1.0 * t)
        
        # Warna dengan variasi alpha untuk efek kedalaman
        alpha = 0.8 - 0.3 * t
        ax.plot(x_hex, y_hex, color="black", linewidth=lw, 
                solid_capstyle="round", zorder=2, alpha=alpha)

    # Framing simetris dengan padding minimal
    cx_final = (min_x + max_x) / 2.0
    cy_final = (min_y + max_y) / 2.0
    w = max_x - min_x
    h = max_y - min_y
    pad = max(w, h) / 2.0 + 1.5  # Padding minimal

    ax.set_xlim(cx_final - pad, cx_final + pad)
    ax.set_ylim(cy_final - pad, cy_final + pad)

    save(fig, "hexagon spiral tight coiled")


if __name__ == "__main__":
    hexagon_spiral_tight_coiled()