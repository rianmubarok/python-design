import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from pathlib import Path
from datetime import datetime

# Konfigurasi Output
SIZE = 4000
DPI = 300
DATE = datetime.now().strftime("%d%m%Y")

# Manajemen Direktori
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
EPS_DIR = OUTPUT_DIR / "eps"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)
EPS_DIR.mkdir(parents=True, exist_ok=True)


def setup_ax():
    """Inisialisasi koordinat axis (off, aspect equal, background putih)."""
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    """Menyimpan gambar dalam format JPG dan SVG."""
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    eps_path = EPS_DIR / f"{name} {DATE}.eps"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    # Save EPS with larger figure size for 4MP+ bounding box
    orig_size = fig.get_size_inches()
    fig.set_size_inches(30, 30)
    fig.savefig(eps_path, format="eps", pad_inches=0, facecolor="white", dpi=DPI)
    fig.set_size_inches(orig_size[0], orig_size[1])
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path} | {eps_path}")


def draw():
    """
    Magnetic Field Dipole Repulsion (Fixed Warp Geometry).
    Concentric circles deformed by two repelling magnetic poles, 
    calculated properly so each vertex remains in a cohesive loop.
    """
    fig, ax = setup_ax()

    # Parameter Pusat Kanvas
    cx, cy = 50.0, 50.0
    
    # Parameter Kisi Lingkaran (Rods)
    n_circles = 45
    max_radius = 65.0
    # Parameter Ketelitian Lingkaran (Vertices per ring)
    n_pts = 600
    
    # Parameter Dua Kutub Tolak-Menolak (Dipole Repulsion)
    # Diposisikan secara horizontal simetris terhadap pusat
    pole1 = np.array([40.0, 50.0])
    pole2 = np.array([60.0, 50.0])
    # Kekuatan Tolakan (Gaya inverse square)
    pole_strength = 200.0
    # Batas jarak minimum untuk menghindari pembagian dengan nol
    min_dist_limit = 3.0

    # Iterasi melalui setiap lingkaran konsentris
    for i in range(1, n_circles + 1):
        # Hitung jari-jari dasar bersih
        r_base = max_radius * (i / n_circles)
        
        # Buat koordinat sudut bersih
        angles = np.linspace(0, 2 * np.pi, n_pts)
        
        # Hitung koordinat x, y dasar bersih
        x_base = r_base * np.cos(angles)
        y_base = r_base * np.sin(angles)
        
        # Inisialisasi array untuk titik sudut yang telah dideformasi
        x_warped = np.zeros(n_pts)
        y_warped = np.zeros(n_pts)
        
        # Hitung deformasi per titik sudut
        for j in range(n_pts):
            # Posisi titik sudut bersih relatif terhadap pusat
            pt_base = np.array([x_base[j], y_base[j]])
            # Posisi absolut titik sudut bersih di kanvas
            pt_canvas = np.array([cx + pt_base[0], cy + pt_base[1]])
            
            # Hitung tolakan dari Kutub 1
            d1_vec = pt_canvas - pole1
            dist1 = np.linalg.norm(d1_vec)
            dist1 = max(dist1, min_dist_limit) # Terapkan batas minimum
            push1 = (d1_vec / dist1) * (pole_strength / (dist1 ** 2))
            
            # Hitung tolakan dari Kutub 2
            d2_vec = pt_canvas - pole2
            dist2 = np.linalg.norm(d2_vec)
            dist2 = max(dist2, min_dist_limit) # Terapkan batas minimum
            push2 = (d2_vec / dist2) * (pole_strength / (dist2 ** 2))
            
            # Terapkan gaya tolakan pada posisi dasar
            x_warped[j] = pt_base[0] + push1[0] + push2[0]
            y_warped[j] = pt_base[1] + push1[1] + push2[1]
        
        # Hitung posisi absolut titik sudut yang telah dideformasi di kanvas
        x_final = cx + x_warped
        y_final = cy + y_warped
        
        # Gunakan LineCollection untuk rendering garis yang mulus dan cepat
        # (Alih-alih plot tunggal per segmen)
        # 1. Konversi koordinat x, y menjadi array segmen (reshape (-1, 1, 2))
        points = np.array([x_final, y_final]).T.reshape(-1, 1, 2)
        # 2. Gabungkan titik berurutan menjadi segmen garis
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        # 3. Tentukan ketebalan garis (linewidth konstan untuk estetika grid)
        lw = 1.0
        
        # 4. Inisialisasi dan konfigurasi LineCollection
        lc = LineCollection(segments, linewidths=lw, colors="black")
        
        # 5. Tambahkan koleksi garis ke kanvas
        ax.add_collection(lc)

    # Simpan hasil dalam format JPG dan SVG
    save(fig, "abstract concentric magnetic field dipole repulsion pattern black white texture")


if __name__ == "__main__":
    draw()