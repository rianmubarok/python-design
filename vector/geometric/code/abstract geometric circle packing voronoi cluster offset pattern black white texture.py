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

SCRIPT DIR = Path(  file  ).resolve().parent
OUTPUT DIR = SCRIPT DIR.parent / "output"
JPG DIR = OUTPUT DIR / "jpg"
SVG DIR = OUTPUT DIR / "svg"
JPG DIR.mkdir(parents=True, exist ok=True)
SVG DIR.mkdir(parents=True, exist ok=True)

np.random.seed(SEED)


def setup ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots adjust(left=0, right=1, top=1, bottom=0)
    ax.set facecolor("white")
    ax.set aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg path = JPG DIR / f"{name} {DATE}.jpg"
    svg path = SVG DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg path, dpi=DPI, pad inches=0, facecolor="white")
    fig.savefig(svg path, format="svg", pad inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg path} | {svg path}")


def circle packing voronoi cluster offset():
    """Circle packing dengan kluster titik yang berpindah dari pusat."""
    fig, ax = setup ax()

    # Buat beberapa kluster titik dengan pusat yang berbeda
    cluster centers = [
        (40, 40),  # Kiri atas
        (60, 40),  # Kanan atas
        (40, 60),  # Kiri bawah
        (60, 60),  # Kanan bawah
        (50, 50),  # Tengah (lebih jarang)
    ]
    
    all points = []
    
    for cx, cy in cluster centers:
        # Buat titik di sekitar pusat kluster
        n points in cluster = 25 if (cx, cy) == (50, 50) else 40
        
        for   in range(n points in cluster):
            # Distribusi Gaussian untuk membuat kluster yang padat
            x = cx + np.random.normal(0, 8)
            y = cy + np.random.normal(0, 8)
            
            # Pastikan titik dalam batas kanvas
            x = max(10, min(90, x))
            y = max(10, min(90, y))
            
            all points.append([x, y])
    
    points = np.array(all points)
    
    # Filter titik untuk jarak minimum
    valid points = []
    min dist threshold = 5.5
    
    for pt in points:
        if not valid points:
            valid points.append(pt)
        else:
            dists = [np.linalg.norm(pt - p) for p in valid points]
            if min(dists) >= min dist threshold:
                valid points.append(pt)
    
    points = np.array(valid points)
    n points = len(points)

    # Tambahkan titik pembatas luar
    grid bounds = np.array([
        [-40, -40], [140, -40], [140, 140], [-40, 140],
        [50, -40], [140, 50], [50, 140], [-40, 50]
    ])
    all points for voronoi = np.vstack([points, grid bounds])
    vor = Voronoi(all points for voronoi)

    # Gambar sel Voronoi dengan gaya yang berbeda
    for simplex in vor.ridge vertices:
        if -1 not in simplex:
            p1 = vor.vertices[simplex[0]]
            p2 = vor.vertices[simplex[1]]
            if (-15 <= p1[0] <= 115 and -15 <= p1[1] <= 115 and
                -15 <= p2[0] <= 115 and -15 <= p2[1] <= 115):
                
                # Tentukan ketebalan berdasarkan posisi
                center x = (p1[0] + p2[0]) / 2
                center y = (p1[1] + p2[1]) / 2
                
                # Garis lebih tebal di dekat pusat kluster
                thickness multiplier = 0
                for cx, cy in cluster centers:
                    dist = np.sqrt((center x - cx)**2 + (center y - cy)**2)
                    if dist < 15:
                        thickness multiplier += 0.3
                
                lw = 0.5 + thickness multiplier
                alpha = 0.4 + 0.2 * thickness multiplier
                
                ax.plot(
                    [p1[0], p2[0]], [p1[1], p2[1]],
                    color="black", linewidth=lw, alpha=alpha, 
                    linestyle=(0, (3, 2)), zorder=1
                )

    # Hitung radius optimal dengan variasi berdasarkan kluster
    radii = np.zeros(n points)
    for i in range(n points):
        # Tentukan kluster terdekat
        cx, cy = points[i]
        cluster distances = [np.sqrt((cx - ccx)**2 + (cy - ccy)**2) for ccx, ccy in cluster centers]
        closest cluster idx = np.argmin(cluster distances)
        
        # Jarak ke titik tetangga terdekat
        dists = [np.linalg.norm(points[i] - points[j]) for j in range(n points) if i != j]
        r neighbor = min(dists) * 0.45  # Lebih rapat di kluster
        
        # Jarak ke batas sel Voronoi
        region idx = vor.point region[i]
        region verts = [vor.vertices[v] for v in vor.regions[region idx] if v != -1]

        if region verts:
            r vert = min([np.linalg.norm(points[i] - v) for v in region verts]) * 0.7
            r = min(r neighbor, r vert)
        else:
            r = r neighbor

        # Radius lebih besar di pusat kluster
        base radius = max(1.2, r)
        if cluster distances[closest cluster idx] < 8:
            radii[i] = base radius * 1.1
        else:
            radii[i] = base radius

    # Gambar Lingkaran dengan variasi
    t = np.linspace(0, 2 * np.pi, 80)
    for i in range(n points):
        cx, cy = points[i]
        r = radii[i]

        x circ = cx + r * np.cos(t)
        y circ = cy + r * np.sin(t)

        # Tentukan gaya berdasarkan posisi relatif terhadap kluster
        cluster distances = [np.sqrt((cx - ccx)**2 + (cy - ccy)**2) for ccx, ccy in cluster centers]
        min dist = min(cluster distances)
        
        if min dist < 5:
            lw = 1.5
            alpha = 0.9
        elif min dist < 15:
            lw = 1.2
            alpha = 0.8
        else:
            lw = 0.9
            alpha = 0.7
        
        ax.plot(x circ, y circ, color="black", linewidth=lw, 
                solid capstyle="round", zorder=2, alpha=alpha)
        
        # Titik pusat dengan variasi ukuran
        marker size = 2.0 if min dist < 10 else 1.2
        ax.plot(cx, cy, marker="o", markersize=marker size, 
                color="black", zorder=3, alpha=0.8)

    # Framing simetris
    pad = 46.0
    ax.set xlim(50 - pad, 50 + pad)
    ax.set ylim(50 - pad, 50 + pad)

    save(fig, "abstract geometric circle packing voronoi cluster offset pattern black white texture"))


if   name   == "  main  ":
    circle packing voronoi cluster offset()