import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path
from datetime import datetime

# Konfigurasi Output
SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

# Penanganan Path (Menghindari spasi pada nama file jika perlu)
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    # PERBAIKAN: top= top=1 diubah menjadi top=1
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    # Membersihkan nama file dari karakter yang mungkin bermasalah
    clean_name = name.replace(" ", "_")
    jpg_path = JPG_DIR / f"{clean_name}_{DATE}.jpg"
    svg_path = SVG_DIR / f"{clean_name}_{DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def draw():
    """Isometric cube grid tessellation with precisely aligned filleted top faces."""
    fig, ax = setup_ax()

    # Parameter Geometri Dasar (Konstan agar tessellation rapat)
    s_base = 6.0  # Ukuran dasar rusuk kubus isometrik
    dx = s_base * np.sqrt(3)  # Jarak antar kolom penuh
    dy = s_base * 1.5          # Jarak antar baris penuh

    # Vektor proyeksi isometrik 3D ke 2D
    # Digunakan untuk menghitung simpul muka
    p1 = np.array([0, s_base])
    p2 = np.array([s_base * np.sqrt(3) / 2, s_base / 2])
    p3 = np.array([s_base * np.sqrt(3) / 2, -s_base / 2])
    p4 = np.array([0, -s_base])
    p5 = np.array([-s_base * np.sqrt(3) / 2, -s_base / 2])
    p6 = np.array([-s_base * np.sqrt(3) / 2, s_base / 2])

    n_rows, n_cols = 16, 16
    
    # Hitung pusat untuk fit_view nanti
    grid_center_x = (n_cols - 1) * dx / 2.0
    grid_center_y = (n_rows - 1) * dy / 2.0

    for row in range(n_rows):
        for col in range(n_cols):
            # Posisi kisi isometrik yang saling mengunci rapat
            cx = col * dx + (dx / 2.0 if row % 2 else 0.0)
            cy = row * dy

            o = np.array([cx, cy])

            # 1. Muka Atas (White with precisely aligned filleted fillet)
            ax.add_patch(
                Polygon(
                    o + np.array([[0, 0], p2 - p1, p2, p1]),
                    closed=True,
                    facecolor="white",
                    edgecolor="black",
                    linewidth=1.0,
                    zorder=2,
                )
            )

            # 2. Muka Kanan (White with Hatching)
            ax.add_patch(
                Polygon(
                    o + np.array([[0, 0], p2, p3, p3 - p2]),
                    closed=True,
                    facecolor="white",
                    edgecolor="black",
                    linewidth=1.0,
                    hatch="////",
                    zorder=2,
                )
            )

            # 3. Muka Kiri (Black Solid)
            ax.add_patch(
                Polygon(
                    o + np.array([[0, 0], p3 - p2, p5, p6]),
                    closed=True,
                    facecolor="black",
                    edgecolor="black",
                    linewidth=1.0,
                    zorder=2,
                )
            )

            # 4. Fillet terproyeksi isometrik di muka atas
            # Parameter kelengkungan (p) berubah berdasarkan modulasi gelombang sine field
            p_val = 1.8 + 1.2 * (0.5 + 0.5 * np.sin((col + row) * 0.35))
            t = np.linspace(0, 2 * np.pi, 60)
            
            # Radius fillet yang disesuaikan dengan kompresi isometrik (terpipihkan)
            rx, ry = s_base * 0.35, s_base * 0.22 

            # Koordinat fillet superellipse (fillet top)
            sq_x = rx * np.sign(np.cos(t)) * (np.abs(np.cos(t)) ** (2 / p_val))
            sq_y = ry * np.sign(np.sin(t)) * (np.abs(np.sin(t)) ** (2 / p_val))

            # Posisi fillet di tengah muka atas kubus
            fillet_cx = cx
            fillet_cy = cy + s_base * 0.5

            ax.plot(
                fillet_cx + sq_x,
                fillet_cy + sq_y,
                color="black",
                linewidth=0.8,
                zorder=3,
            )

    # Tangkapan area tengah penuh dan simetris (fit_view manual)
    pad = 38.0
    ax.set_xlim(grid_center_x - pad, grid_center_x + pad)
    ax.set_ylim(grid_center_y - pad, grid_center_y + pad)

    save(
        fig,
        "abstract grid tessellation isometric cube rounded top fillet pattern black white texture",
    )


if __name__ == "__main__":
    draw()