import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, RegularPolygon
from pathlib import Path
from datetime import datetime

# Konfigurasi Output
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
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi= DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    # Membersihkan nama file dari spasi
    clean_name = name.replace(" ", "_")
    jpg_path = JPG_DIR / f"{clean_name}_{DATE}.jpg"
    svg_path = SVG_DIR / f"{clean_name}_{DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def draw():
    """Tessellated honeycomb network with precisely interlocking Wang-style pipes."""
    fig, ax = setup_ax()
    
    # Parameter Kisi Heksagonal
    r = 7.5  # Radius rusuk heksagon
    dx = r * np.sqrt(3) # Jarak antar-kolom penuh
    dy = r * 1.5         # Jarak antar-baris penuh

    rows, cols = 15, 15
    center_x = (cols - 1) * dx / 2.0
    center_y = (rows - 1) * dy / 2.0
    
    # 1. Plot Kisi Heksagon Jaring Madu (Penuh tanpa terputus)
    # Gunakan orientasi 30 deg (np.pi/6) agar kisi sejajar rapat
    for row in range(rows):
        for col in range(cols):
            # Posisi kisi isometrik selang-seling (Honeycomb tessellation)
            cx = col * dx + (dx / 2.0 if row % 2 else 0.0)
            cy = row * dy
            
            # Tambahkan patch sel penuh tanpa tumpang tindih
            ax.add_patch(
                RegularPolygon(
                    (cx, cy),
                    6,
                    radius=r,
                    orientation=np.pi / 6,
                    fill=False,
                    edgecolor="black",
                    linewidth=0.8,
                    zorder=1,
                )
            )

    # 2. Plot Jaringan Pipa Wang Terintegrasi (Terhubung secara mulus)
    # Tipe-tipe pipa Wang sejati yang saling mengunci rapat:
    # 0: H-straight, 1: V-straight, 2: TL-elbow, 3: TR-elbow, 4: BL-elbow, 5: BR-elbow
    # Gunakan bobot garis dinamis selang-seling
    def get_pipe_pts(cx, cy, r, ptype):
        step_ang = np.pi / 3.0
        # Simpul untuk koneksi tepi (edge centers)
        edges = []
        for k in range(6):
            ang = (k + 0.5) * step_ang + np.pi / 6.0
            edges.append([cx + r * np.cos(ang), cy + r * np.sin(ang)])
        
        verts = np.array(edges)
        
        if ptype == 0:  # Horizontal straight
            return [verts[3], verts[0]]
        elif ptype == 1:  # Vertical straight
            return [verts[1], verts[4]]
        elif ptype == 2:  # Elbow Top-Left
            return [verts[2], verts[3]]
        elif ptype == 3:  # Elbow Top-Right
            return [verts[0], verts[1]]
        elif ptype == 4:  # Elbow Bottom-Left
            return [verts[4], verts[5]]
        else:  # Elbow Bottom-Right
            return [verts[5], verts[0]]

    # Gunakan SEED agar acak namun reproduksibel
    rng = np.random.default_rng(SEED)

    for row in range(rows):
        for col in range(cols):
            cx = col * dx + (dx / 2.0 if row % 2 else 0.0)
            cy = row * dy
            
            # Bobot garis dinamis (Pulsing thickness wave)
            thick = 1.4 + 2.4 * (0.5 + 0.5 * np.sin(col * 0.7) * np.cos(row * 0.55))
            
            # Tentukan tipe pipa untuk sel ini agar interlocking sempurna
            # Saling mengunci: H-Straight kunci tepi kiri/kanan, V-Straight kunci tepi atas/bawah, dll.
            ptype = rng.integers(0, 6)
            
            # Plot Pipa Tumpuk (H-straight di bawah, yang lain di atas)
            p_verts = get_pipe_pts(cx, cy, r, ptype)
            p_verts_w = np.array(p_verts) * 1.01 # Lebarkan sedikit agar visual tumpuk jelas

            ax.add_patch(
                Polygon(
                    p_verts_w,
                    closed=True,
                    facecolor="none",
                    edgecolor="black",
                    linewidth=thick,
                    linestyle="-",
                    zorder=2,
                )
            )
            ax.add_patch(
                Polygon(
                    p_verts,
                    closed=True,
                    facecolor="white", # Isi putih agar menutupi garis kisi di bawahnya
                    edgecolor="black",
                    linewidth=thick,
                    linestyle="-",
                    zorder=3,
                )
            )

    # Tangkapan area tengah penuh dan simetris
    pad = 38.0
    ax.set_xlim(center_x - pad, center_x + pad)
    ax.set_ylim(center_y - pad, center_y + pad)

    save(
        fig,
        "abstract grid tessellation honeycomb edge wang pipe fusion pattern black white texture",
    )


if __name__ == "__main__":
    # Gunakan SEED agar acak namun reproduksibel
    SEED = 4
    draw()