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
    jpg_path = JPG_DIR / f"{name}_{DATE}.jpg"
    svg_path = SVG_DIR / f"{name}_{DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def draw_rounded_polygon(ax, center_x, center_y, size, n_sides, corner_radius, rotation=0):
    """Menggambar poligon dengan sudut membulat."""
    angles = np.linspace(0, 2 * np.pi, n_sides + 1)
    
    # Titik sudut poligon reguler
    points = []
    for angle in angles[:-1]:
        x = center_x + size * np.cos(angle + rotation)
        y = center_y + size * np.sin(angle + rotation)
        points.append((x, y))
    
    # Gambar poligon dengan garis lurus (tanpa kurva)
    xs = [p[0] for p in points] + [points[0][0]]
    ys = [p[1] for p in points] + [points[0][1]]
    
    return xs, ys, points


def rounded_polygon_morph_corner_radius():
    """Poligon dengan jumlah sisi dan radius sudut yang bermetamorfosis."""
    fig, ax = setup_ax()
    
    center_x, center_y = 50, 50
    n_shapes = 24
    
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    
    for i in range(n_shapes):
        t = i / (n_shapes - 1)
        
        # Ukuran bertambah
        size = 5 + i * 1.8
        
        # Jumlah sisi bermetamorfosis dari segitiga (3) ke banyak sisi (~12)
        n_sides = int(3 + 9 * t)
        
        # Radius sudut bermetamorfosis dari tajam ke sangat membulat
        # Gunakan fungsi sigmoid untuk transisi yang halus
        corner_radius_factor = 1 / (1 + np.exp(-10 * (t - 0.5)))
        corner_radius = size * 0.15 * corner_radius_factor
        
        # Rotasi bertambah
        rotation = i * 0.3
        
        # Gambar poligon
        xs, ys, points = draw_rounded_polygon(ax, center_x, center_y, 
                                              size, n_sides, corner_radius, rotation)
        
        # Gambar poligon utama
        lw = 0.8 + 1.5 * t
        alpha = 0.9 - 0.3 * t
        
        ax.plot(xs, ys, color="black", linewidth=lw, alpha=alpha)
        
        # Tambahkan lingkaran di sudut untuk efek radius yang visual
        if corner_radius > size * 0.05:
            for px, py in points:
                # Hitung posisi efektif dengan radius
                angle_to_center = np.arctan2(py - center_y, px - center_x)
                effective_x = center_x + (size - corner_radius * 0.7) * np.cos(angle_to_center)
                effective_y = center_y + (size - corner_radius * 0.7) * np.sin(angle_to_center)
                
                circle = plt.Circle((effective_x, effective_y), corner_radius * 0.3,
                                   fill=False, linewidth=0.4, 
                                   edgecolor="black", alpha=0.4)
                ax.add_patch(circle)
        
        # Gambar lingkaran batin untuk menunjukkan transisi
        inner_size = size * 0.6
        inner_circle = plt.Circle((center_x, center_y), inner_size,
                                 fill=False, linewidth=0.5, 
                                 edgecolor="black", alpha=0.3, linestyle="--")
        ax.add_patch(inner_circle)
        
        # Melacak bounding box
        for px, py in points:
            # Perhitungkan radius sudut dalam bounding box
            adjusted_x = px + corner_radius if px > center_x else px - corner_radius
            adjusted_y = py + corner_radius if py > center_y else py - corner_radius
            
            min_x, max_x = min(min_x, adjusted_x), max(max_x, adjusted_x)
            min_y, max_y = min(min_y, adjusted_y), max(max_y, adjusted_y)
    
    # Tambahkan pusat spiral untuk penekanan
    for i in range(8):
        spiral_radius = 2 + i * 0.5
        spiral_angle = i * 0.8
        spiral_x = center_x + spiral_radius * np.cos(spiral_angle)
        spiral_y = center_y + spiral_radius * np.sin(spiral_angle)
        ax.plot(spiral_x, spiral_y, marker="o", markersize=0.8, 
                color="black", alpha=0.7)
    
    # Framing dinamis
    cx_final = (min_x + max_x) / 2.0
    cy_final = (min_y + max_y) / 2.0
    w = max_x - min_x
    h = max_y - min_y
    pad = max(w, h) / 2.0 + 3.0
    
    ax.set_xlim(cx_final - pad, cx_final + pad)
    ax.set_ylim(cy_final - pad, cy_final + pad)
    
    save(fig, "rounded polygon morph corner radius")


if __name__ == "__main__":
    rounded_polygon_morph_corner_radius()