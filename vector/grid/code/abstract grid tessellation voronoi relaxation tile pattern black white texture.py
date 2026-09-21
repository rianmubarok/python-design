import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path
from datetime import datetime
from scipy.spatial import Voronoi  # <-- Tambahkan library ini untuk tessellation asli

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
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
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


def abstract_grid_tessellation_voronoi_relaxation_tile_pattern_black_white_texture():
    """Tweak: Menghasilkan pola ubin sel Voronoi asli dengan efek relaksasi Lloyd."""
    fig, ax = setup_ax()
    
    # 1. Generate seed points di area tengah agar sel pinggir tidak pecah ke tak terhingga
    n_seeds = 35
    seeds = np.random.uniform(5, 95, size=(n_seeds, 2))
    
    # 2. Lloyd's Relaxation (10 iterasi untuk membuat jarak antar titik lebih seragam/organik)
    for _ in range(10):
        vor = Voronoi(seeds)
        new_seeds = []
        for i, region_idx in enumerate(vor.point_region):
            region = vor.regions[region_idx]
            # Pastikan region tertutup (tidak ada indeks -1)
            if not region or -1 in region:
                new_seeds.append(seeds[i])
                continue
            polygon = vor.vertices[region]
            # Hitung titik berat (centroid) sebagai posisi seed baru
            centroid = np.mean(polygon, axis=0)
            new_seeds.append(centroid)
        seeds = np.array(new_seeds)
    
    # 3. Buat ulang Voronoi akhir setelah proses relaksasi selesai
    vor = Voronoi(seeds)
    
    # 4. Gambar ubin konsentris di dalam setiap sel Voronoi yang valid
    for region_idx in vor.point_region:
        region = vor.regions[region_idx]
        if not region or -1 in region:
            continue
            
        vertices = vor.vertices[region]
        centroid = np.mean(vertices, axis=0)
        
        # Buat cincin konsentris dari arah luar mengecil ke dalam (skala 0.95 down to 0.2)
        for scale in np.linspace(0.95, 0.2, 5):
            # Skalakan sudut poligon mendekati titik pusat sel (centroid)
            scaled_vertices = centroid + (vertices - centroid) * scale
            
            poly = Polygon(scaled_vertices, fill=False, edgecolor="black", linewidth=0.8)
            ax.add_patch(poly)

    save(fig, "abstract grid tessellation voronoi relaxation tile pattern black white texture")


if __name__ == "__main__":
    abstract_grid_tessellation_voronoi_relaxation_tile_pattern_black_white_texture()
