import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.transforms import Affine2D
from pathlib import Path
from datetime import datetime

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


def draw rounded polygon(ax, center x, center y, size, n sides, corner radius, rotation=0):
    """Menggambar poligon dengan sudut membulat."""
    angles = np.linspace(0, 2 * np.pi, n sides + 1)
    
    # Titik sudut poligon reguler
    points = []
    for angle in angles[:-1]:
        x = center x + size * np.cos(angle + rotation)
        y = center y + size * np.sin(angle + rotation)
        points.append((x, y))
    
    # Gambar poligon dengan garis lurus (tanpa kurva)
    xs = [p[0] for p in points] + [points[0][0]]
    ys = [p[1] for p in points] + [points[0][1]]
    
    return xs, ys, points


def rounded polygon morph corner radius():
    """Poligon dengan jumlah sisi dan radius sudut yang bermetamorfosis."""
    fig, ax = setup ax()
    
    center x, center y = 50, 50
    n shapes = 24
    
    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")
    
    for i in range(n shapes):
        t = i / (n shapes - 1)
        
        # Ukuran bertambah
        size = 5 + i * 1.8
        
        # Jumlah sisi bermetamorfosis dari segitiga (3) ke banyak sisi (~12)
        n sides = int(3 + 9 * t)
        
        # Radius sudut bermetamorfosis dari tajam ke sangat membulat
        # Gunakan fungsi sigmoid untuk transisi yang halus
        corner radius factor = 1 / (1 + np.exp(-10 * (t - 0.5)))
        corner radius = size * 0.15 * corner radius factor
        
        # Rotasi bertambah
        rotation = i * 0.3
        
        # Gambar poligon
        xs, ys, points = draw rounded polygon(ax, center x, center y, 
                                              size, n sides, corner radius, rotation)
        
        # Gambar poligon utama
        lw = 0.8 + 1.5 * t
        alpha = 0.9 - 0.3 * t
        
        ax.plot(xs, ys, color="black", linewidth=lw, alpha=alpha)
        
        # Tambahkan lingkaran di sudut untuk efek radius yang visual
        if corner radius > size * 0.05:
            for px, py in points:
                # Hitung posisi efektif dengan radius
                angle to center = np.arctan2(py - center y, px - center x)
                effective x = center x + (size - corner radius * 0.7) * np.cos(angle to center)
                effective y = center y + (size - corner radius * 0.7) * np.sin(angle to center)
                
                circle = plt.Circle((effective x, effective y), corner radius * 0.3,
                                   fill=False, linewidth=0.4, 
                                   edgecolor="black", alpha=0.4)
                ax.add patch(circle)
        
        # Gambar lingkaran batin untuk menunjukkan transisi
        inner size = size * 0.6
        inner circle = plt.Circle((center x, center y), inner size,
                                 fill=False, linewidth=0.5, 
                                 edgecolor="black", alpha=0.3, linestyle="--")
        ax.add patch(inner circle)
        
        # Melacak bounding box
        for px, py in points:
            # Perhitungkan radius sudut dalam bounding box
            adjusted x = px + corner radius if px > center x else px - corner radius
            adjusted y = py + corner radius if py > center y else py - corner radius
            
            min x, max x = min(min x, adjusted x), max(max x, adjusted x)
            min y, max y = min(min y, adjusted y), max(max y, adjusted y)
    
    # Tambahkan pusat spiral untuk penekanan
    for i in range(8):
        spiral radius = 2 + i * 0.5
        spiral angle = i * 0.8
        spiral x = center x + spiral radius * np.cos(spiral angle)
        spiral y = center y + spiral radius * np.sin(spiral angle)
        ax.plot(spiral x, spiral y, marker="o", markersize=0.8, 
                color="black", alpha=0.7)
    
    # Framing dinamis
    cx final = (min x + max x) / 2.0
    cy final = (min y + max y) / 2.0
    w = max x - min x
    h = max y - min y
    pad = max(w, h) / 2.0 + 3.0
    
    ax.set xlim(cx final - pad, cx final + pad)
    ax.set ylim(cy final - pad, cy final + pad)
    
    save(fig, "abstract geometric rounded polygon morph corner radius pattern black white texture"))


if   name   == "  main  ":
    rounded polygon morph corner radius()