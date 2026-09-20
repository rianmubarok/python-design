from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Voronoi
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


def circle_packing_voronoi_cluster_offset():
    """Circle packing dengan kluster titik yang berpindah dari pusat."""
    fig, ax = setup_ax()

    # Buat beberapa kluster titik dengan pusat yang berbeda
    cluster_centers = [
        (40, 40),  # Kiri atas
        (60, 40),  # Kanan atas
        (40, 60),  # Kiri bawah
        (60, 60),  # Kanan bawah
        (50, 50),  # Tengah (lebih jarang)
    ]
    
    all_points = []
    
    for cx, cy in cluster_centers:
        # Buat titik di sekitar pusat kluster
        n_points_in_cluster = 25 if (cx, cy) == (50, 50) else 40
        
        for _ in range(n_points_in_cluster):
            # Distribusi Gaussian untuk membuat kluster yang padat
            x = cx + np.random.normal(0, 8)
            y = cy + np.random.normal(0, 8)
            
            # Pastikan titik dalam batas kanvas
            x = max(10, min(90, x))
            y = max(10, min(90, y))
            
            all_points.append([x, y])
    
    points = np.array(all_points)
    
    # Filter titik untuk jarak minimum
    valid_points = []
    min_dist_threshold = 5.5
    
    for pt in points:
        if not valid_points:
            valid_points.append(pt)
        else:
            dists = [np.linalg.norm(pt - p) for p in valid_points]
            if min(dists) >= min_dist_threshold:
                valid_points.append(pt)
    
    points = np.array(valid_points)
    n_points = len(points)

    # Tambahkan titik pembatas luar
    grid_bounds = np.array([
        [-40, -40], [140, -40], [140, 140], [-40, 140],
        [50, -40], [140, 50], [50, 140], [-40, 50]
    ])
    all_points_for_voronoi = np.vstack([points, grid_bounds])
    vor = Voronoi(all_points_for_voronoi)

    # Gambar sel Voronoi dengan gaya yang berbeda
    for simplex in vor.ridge_vertices:
        if -1 not in simplex:
            p1 = vor.vertices[simplex[0]]
            p2 = vor.vertices[simplex[1]]
            if (-15 <= p1[0] <= 115 and -15 <= p1[1] <= 115 and
                -15 <= p2[0] <= 115 and -15 <= p2[1] <= 115):
                
                # Tentukan ketebalan berdasarkan posisi
                center_x = (p1[0] + p2[0]) / 2
                center_y = (p1[1] + p2[1]) / 2
                
                # Garis lebih tebal di dekat pusat kluster
                thickness_multiplier = 0
                for cx, cy in cluster_centers:
                    dist = np.sqrt((center_x - cx)**2 + (center_y - cy)**2)
                    if dist < 15:
                        thickness_multiplier += 0.3
                
                lw = 0.5 + thickness_multiplier
                alpha = 0.4 + 0.2 * thickness_multiplier
                
                ax.plot(
                    [p1[0], p2[0]], [p1[1], p2[1]],
                    color="black", linewidth=lw, alpha=alpha, 
                    linestyle=(0, (3, 2)), zorder=1
                )

    # Hitung radius optimal dengan variasi berdasarkan kluster
    radii = np.zeros(n_points)
    for i in range(n_points):
        # Tentukan kluster terdekat
        cx, cy = points[i]
        cluster_distances = [np.sqrt((cx - ccx)**2 + (cy - ccy)**2) for ccx, ccy in cluster_centers]
        closest_cluster_idx = np.argmin(cluster_distances)
        
        # Jarak ke titik tetangga terdekat
        dists = [np.linalg.norm(points[i] - points[j]) for j in range(n_points) if i != j]
        r_neighbor = min(dists) * 0.45  # Lebih rapat di kluster
        
        # Jarak ke batas sel Voronoi
        region_idx = vor.point_region[i]
        region_verts = [vor.vertices[v] for v in vor.regions[region_idx] if v != -1]

        if region_verts:
            r_vert = min([np.linalg.norm(points[i] - v) for v in region_verts]) * 0.7
            r = min(r_neighbor, r_vert)
        else:
            r = r_neighbor

        # Radius lebih besar di pusat kluster
        base_radius = max(1.2, r)
        if cluster_distances[closest_cluster_idx] < 8:
            radii[i] = base_radius * 1.1
        else:
            radii[i] = base_radius

    # Gambar Lingkaran dengan variasi
    t = np.linspace(0, 2 * np.pi, 80)
    for i in range(n_points):
        cx, cy = points[i]
        r = radii[i]

        x_circ = cx + r * np.cos(t)
        y_circ = cy + r * np.sin(t)

        # Tentukan gaya berdasarkan posisi relatif terhadap kluster
        cluster_distances = [np.sqrt((cx - ccx)**2 + (cy - ccy)**2) for ccx, ccy in cluster_centers]
        min_dist = min(cluster_distances)
        
        if min_dist < 5:
            lw = 1.5
            alpha = 0.9
        elif min_dist < 15:
            lw = 1.2
            alpha = 0.8
        else:
            lw = 0.9
            alpha = 0.7
        
        ax.plot(x_circ, y_circ, color="black", linewidth=lw, 
                solid_capstyle="round", zorder=2, alpha=alpha)
        
        # Titik pusat dengan variasi ukuran
        marker_size = 2.0 if min_dist < 10 else 1.2
        ax.plot(cx, cy, marker="o", markersize=marker_size, 
                color="black", zorder=3, alpha=0.8)

    # Framing simetris
    pad = 46.0
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)

    save(fig, "circle packing voronoi cluster offset")


if __name__ == "__main__":
    circle_packing_voronoi_cluster_offset()