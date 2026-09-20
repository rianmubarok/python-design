from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.use("Agg")

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


def subdivide_triangle(p1, p2, p3, depth, max_depth, ax):
    """Subdivisi rekursif segitiga Sierpinski dengan bobot garis yang proporsional."""
    if depth >= max_depth:
        return

    # Hitung titik tengah setiap sisi
    mid12 = ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)
    mid23 = ((p2[0] + p3[0]) / 2.0, (p2[1] + p3[1]) / 2.0)
    mid31 = ((p3[0] + p1[0]) / 2.0, (p3[1] + p1[1]) / 2.0)

    lw = max(0.4, 1.8 - depth * 0.3)

    # Plot segitiga tengah yang terbalik
    triangle_x = [mid12[0], mid23[0], mid31[0], mid12[0]]
    triangle_y = [mid12[1], mid23[1], mid31[1], mid12[1]]

    ax.plot(
        triangle_x,
        triangle_y,
        color="black",
        linewidth=lw,
        solid_capstyle="round",
        zorder=2,
    )

    # Rekursi ke 3 segitiga di sudut
    subdivide_triangle(p1, mid12, mid31, depth + 1, max_depth, ax)
    subdivide_triangle(mid12, p2, mid23, depth + 1, max_depth, ax)
    subdivide_triangle(mid31, mid23, p3, depth + 1, max_depth, ax)


def triangle_fractal_subdivision():
    """Teselasi segitiga fraktal yang tersusun rapi, simetris, dan terpusat."""
    fig, ax = setup_ax()

    # Struktur Hexagram / Triforce simetris yang saling menyambung tanpa tumpang tindih
    cx, cy = 50.0, 50.0
    side = 70.0
    h = side * np.sqrt(3) / 2.0

    # Segitiga Utama Besar (Hadap Atas)
    p1 = (cx, cy + (2 / 3) * h)
    p2 = (cx - side / 2.0, cy - (1 / 3) * h)
    p3 = (cx + side / 2.0, cy - (1 / 3) * h)

    # Garis tepi segitiga utama
    ax.plot(
        [p1[0], p2[0], p3[0], p1[0]],
        [p1[1], p2[1], p3[1], p1[1]],
        color="black",
        linewidth=2.2,
        solid_capstyle="round",
        zorder=1,
    )

    # Jalankan subdivisi fraktal hingga kedalaman 5
    subdivide_triangle(p1, p2, p3, 0, 5, ax)

    # Atur tampilan simetris tepat di tengah kanvas
    pad = 42.0
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)

    save(fig, "triangle fractal subdivision")


if __name__ == "__main__":
    triangle_fractal_subdivision()