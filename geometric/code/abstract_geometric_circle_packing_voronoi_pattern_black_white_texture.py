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


def circle_packing_voronoi():
    """Circle packing presisi tanpa tumpang tindih di dalam sel Voronoi."""
    fig, ax = setup_ax()

    # 1. Generate titik-titik dengan jarak minimum yang terkontrol (Poisson-like)
    raw_points = np.random.uniform(10, 90, (150, 2))
    valid_points = []
    min_dist_threshold = 6.0  # Mencegah titik terlalu rapat

    for pt in raw_points:
        if not valid_points:
            valid_points.append(pt)
        else:
            dists = [np.linalg.norm(pt - p) for p in valid_points]
            if min(dists) >= min_dist_threshold:
                valid_points.append(pt)

    points = np.array(valid_points)
    n_points = len(points)

    # Tambahkan titik pembatas luar agar sel Voronoi tepi tertutup simetris
    grid_bounds = np.array([
        [-40, -40], [140, -40], [140, 140], [-40, 140],
        [50, -40], [140, 50], [50, 140], [-40, 50]
    ])
    all_points = np.vstack([points, grid_bounds])
    vor = Voronoi(all_points)

    # 2. Gambar sel Voronoi (Garis Putus-Putus Bersih)
    for simplex in vor.ridge_vertices:
        if -1 not in simplex:
            p1 = vor.vertices[simplex[0]]
            p2 = vor.vertices[simplex[1]]
            if (-15 <= p1[0] <= 115 and -15 <= p1[1] <= 115 and
                -15 <= p2[0] <= 115 and -15 <= p2[1] <= 115):
                ax.plot(
                    [p1[0], p2[0]], [p1[1], p2[1]],
                    color="black", linewidth=0.7, alpha=0.6, linestyle=(0, (4, 3)), zorder=1
                )

    # 3. Hitung radius optimal tanpa tumpang tindih
    radii = np.zeros(n_points)
    for i in range(n_points):
        # Jarak ke titik pusat tetangga terdekat
        dists = [np.linalg.norm(points[i] - points[j]) for j in range(n_points) if i != j]
        r_neighbor = min(dists) * 0.48  # Sedikit di bawah 0.5 agar ada celah halus

        # Jarak ke batas sel Voronoi
        region_idx = vor.point_region[i]
        region_verts = [vor.vertices[v] for v in vor.regions[region_idx] if v != -1]

        if region_verts:
            r_vert = min([np.linalg.norm(points[i] - v) for v in region_verts]) * 0.75
            r = min(r_neighbor, r_vert)
        else:
            r = r_neighbor

        radii[i] = max(1.5, r)

    # 4. Gambar Lingkaran & Titik Pusat
    t = np.linspace(0, 2 * np.pi, 100)
    for i in range(n_points):
        cx, cy = points[i]
        r = radii[i]

        x_circ = cx + r * np.cos(t)
        y_circ = cy + r * np.sin(t)

        ax.plot(x_circ, y_circ, color="black", linewidth=1.2, solid_capstyle="round", zorder=2)
        ax.plot(cx, cy, marker="o", markersize=1.8, color="black", zorder=3)

    # Framing simetris terpusat di tengah kanvas
    pad = 46.0
    ax.set_xlim(50 - pad, 50 + pad)
    ax.set_ylim(50 - pad, 50 + pad)

    save(fig, "circle packing voronoi")


if __name__ == "__main__":
    circle_packing_voronoi()