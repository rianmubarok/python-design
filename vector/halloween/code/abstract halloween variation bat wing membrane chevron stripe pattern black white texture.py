from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import matplotlib

matplotlib.use("Agg")

SIZE = 4000
DPI = 300
PERIOD = 100.0
DATE = datetime.now().strftime("%d%m%Y")
WRAPS = [(i * PERIOD, j * PERIOD) for i in (-1, 0, 1) for j in (-1, 0, 1)]

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    # Latar belakang diubah menjadi putih sesuai dengan gambar referensi
    ax.set_facecolor("white")
    ax.set_xlim(0, PERIOD)
    ax.set_ylim(0, PERIOD)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    # Memastikan latar belakang saat disave tetap putih
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Saved: {jpg_path} | {svg_path}")


def draw_geometric_bat_chevron(ax, cx, cy, w, h, fill="black"):
    """Menggambar sepasang sayap Chevron geometris kaku (jajar genjang & belah ketupat)."""
    
    polygons = []
    
    # 1. Berlian/Wajik Tengah (Center Diamond)
    p_center = [
        (0, h * 0.42), 
        (w * 0.07, h * 0.12), 
        (0, -h * 0.28), 
        (-w * 0.07, h * 0.12)
    ]
    polygons.append(p_center)
    
    # Fungsi bantu untuk menggandakan bentuk ke sisi kiri (simetri)
    def add_symmetric(poly):
        polygons.append(poly)
        polygons.append([(-x, y) for x, y in poly])

    # 2. Jajar Genjang Sayap Dalam (Inner Parallelogram)
    p_inner_r = [
        (w * 0.11, h * 0.25),
        (w * 0.19, h * 0.02),
        (w * 0.19, -h * 0.38),
        (w * 0.11, -h * 0.15)
    ]
    add_symmetric(p_inner_r)
    
    # 3. Jajar Genjang Sayap Luar (Outer Parallelogram)
    p_outer_r = [
        (w * 0.23, h * 0.05),
        (w * 0.31, -h * 0.18),
        (w * 0.31, -h * 0.45),
        (w * 0.23, -h * 0.22)
    ]
    add_symmetric(p_outer_r)
    
    # 4. Segitiga Kecil Ujung (Bottom Outer Triangle)
    p_tri_r = [
        (w * 0.35, -h * 0.15),
        (w * 0.42, -h * 0.35),
        (w * 0.35, -h * 0.35)
    ]
    add_symmetric(p_tri_r)

    # Render seluruh bagian poligon dengan Wrap Seamless
    for poly in polygons:
        # Geser ke titik pusat cx, cy
        shifted_poly = [(px + cx, py + cy) for px, py in poly]
        
        # Duplikasi ke 9 zona WRAPS untuk memastikan seamless tepi gambar
        for ox, oy in WRAPS:
            final_poly = [(px + ox, py + oy) for px, py in shifted_poly]
            ax.add_patch(Polygon(final_poly, facecolor=fill, edgecolor="none", zorder=2))


def draw():
    """Pola Chevron sayap kelelawar beranyaman presisi dan 100% seamless."""
    fig, ax = setup_ax()

    # Kepadatan grid ditingkatkan agar rasio kepadatannya mirip dengan gambar asli
    cols = 12
    rows = 14
    dx = PERIOD / cols
    dy = PERIOD / rows
    
    w = dx * 1.05
    h = dy * 1.05

    wings_data = []

    for row in range(rows):
        # Gunakan pergeseran horizontal selang-seling (brick pattern staggered grid)
        shift = dx * 0.5 if row % 2 else 0.0
        for col in range(cols):
            cx = col * dx + shift
            cy = (row + 0.5) * dy
            wings_data.append((cx, cy))

    # Render data wajik/sayap utuh di pusat asli [0, PERIOD]
    for cx, cy in wings_data:
        # Panggil fungsi geometris linier, bukan fungsi path melengkung
        draw_geometric_bat_chevron(ax, cx, cy, w, h, fill="black")

    save(fig, "abstract halloween variation bat wing membrane chevron stripe pattern black white texture")


if __name__ == "__main__":
    draw()