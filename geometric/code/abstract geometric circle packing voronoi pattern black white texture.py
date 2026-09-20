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


def circle packing voronoi():
    """Circle packing presisi tanpa tumpang tindih di dalam sel Voronoi."""
    fig, ax = setup ax()

    # 1. Generate titik-titik dengan jarak minimum yang terkontrol (Poisson-like)
    raw points = np.random.uniform(10, 90, (150, 2))
    valid points = []
    min dist threshold = 6.0  # Mencegah titik terlalu rapat

    for pt in raw points:
        if not valid points:
            valid points.append(pt)
        else:
            dists = [np.linalg.norm(pt - p) for p in valid points]
            if min(dists) >= min dist threshold:
                valid points.append(pt)

    points = np.array(valid points)
    n points = len(points)

    # Tambahkan titik pembatas luar agar sel Voronoi tepi tertutup simetris
    grid bounds = np.array([
        [-40, -40], [140, -40], [140, 140], [-40, 140],
        [50, -40], [140, 50], [50, 140], [-40, 50]
    ])
    all points = np.vstack([points, grid bounds])
    vor = Voronoi(all points)

    # 2. Gambar sel Voronoi (Garis Putus-Putus Bersih)
    for simplex in vor.ridge vertices:
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
    radii = np.zeros(n points)
    for i in range(n points):
        # Jarak ke titik pusat tetangga terdekat
        dists = [np.linalg.norm(points[i] - points[j]) for j in range(n points) if i != j]
        r neighbor = min(dists) * 0.48  # Sedikit di bawah 0.5 agar ada celah halus

        # Jarak ke batas sel Voronoi
        region idx = vor.point region[i]
        region verts = [vor.vertices[v] for v in vor.regions[region idx] if v != -1]

        if region verts:
            r vert = min([np.linalg.norm(points[i] - v) for v in region verts]) * 0.75
            r = min(r neighbor, r vert)
        else:
            r = r neighbor

        radii[i] = max(1.5, r)

    # 4. Gambar Lingkaran & Titik Pusat
    t = np.linspace(0, 2 * np.pi, 100)
    for i in range(n points):
        cx, cy = points[i]
        r = radii[i]

        x circ = cx + r * np.cos(t)
        y circ = cy + r * np.sin(t)

        ax.plot(x circ, y circ, color="black", linewidth=1.2, solid capstyle="round", zorder=2)
        ax.plot(cx, cy, marker="o", markersize=1.8, color="black", zorder=3)

    # Framing simetris terpusat di tengah kanvas
    pad = 46.0
    ax.set xlim(50 - pad, 50 + pad)
    ax.set ylim(50 - pad, 50 + pad)

    save(fig, "circle packing voronoi")


if   name   == "  main  ":
    circle packing voronoi()