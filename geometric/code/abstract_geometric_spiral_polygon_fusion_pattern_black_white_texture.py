import numpy as np
import matplotlib.pyplot as plt
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
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def draw_polygon(cx, cy, size, n_sides, rotation=0):
    """Menggambar poligon dengan n sisi."""
    angles = np.linspace(0, 2 * np.pi, n_sides + 1) + rotation
    x = cx + size * np.cos(angles)
    y = cy + size * np.sin(angles)
    return x, y


def spiral_polygon_fusion():
    """Fusi spiral dengan poligon yang bermetamorfosis."""
    fig, ax = setup_ax()
    
    center_x, center_y = 50, 50
    
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    
    # Parameter spiral utama
    n_spiral_points = 120
    spiral_turns = 5.5
    max_radius = 38.0
    
    # Simpan posisi spiral untuk referensi
    spiral_positions = []
    
    # Layer 1: Spiral dasar dengan poligon di setiap titik
    for i in range(n_spiral_points):
        t = i / n_spiral_points
        angle = t * spiral_turns * 2 * np.pi
        radius = 2.0 + max_radius * (t ** 1.2)
        
        spiral_x = center_x + radius * np.cos(angle)
        spiral_y = center_y + radius * np.sin(angle)
        spiral_positions.append((spiral_x, spiral_y, t))
        
        # Jumlah sisi poligon meningkat sepanjang spiral
        # Dari segitiga (3) ke oktagon (8) dan kembali
        n_sides = int(3 + 5 * np.sin(t * np.pi * 2))
        n_sides = max(3, min(8, n_sides))
        
        # Ukuran poligon meningkat sepanjang spiral
        polygon_size = 0.8 + 3.5 * t
        
        # Rotasi poligon mengikuti spiral
        polygon_rotation = angle * 0.8 + t * np.pi
        
        # Gambar poligon
        x_poly, y_poly = draw_polygon(spiral_x, spiral_y, polygon_size, n_sides, polygon_rotation)
        
        # Ketebalan garis berdasarkan posisi spiral
        lw = 0.6 + 1.2 * (1.0 - t)
        alpha = 0.8 - 0.3 * t
        
        ax.plot(x_poly, y_poly, color="black", linewidth=lw, alpha=alpha)
        
        # Update bounding box
        min_x, max_x = min(min_x, x_poly.min()), max(max_x, x_poly.max())
        min_y, max_y = min(min_y, y_poly.min()), max(max_y, y_poly.max())
        
        # Tambahkan titik pusat poligon
        ax.plot(spiral_x, spiral_y, marker="o", markersize=0.6, 
                color="black", alpha=0.6)
    
    # Layer 2: Garis penghubung antara poligon spiral
    for i in range(len(spiral_positions) - 1):
        x1, y1, t1 = spiral_positions[i]
        x2, y2, t2 = spiral_positions[i + 1]
        
        # Gambar garis penghubung dengan pola
        n_segments = 3
        for seg in range(n_segments):
            seg_t1 = seg / n_segments
            seg_t2 = (seg + 1) / n_segments
            
            # Titik di sepanjang garis dengan offset sinusoidal
            seg_x1 = x1 + (x2 - x1) * seg_t1
            seg_y1 = y1 + (y2 - y1) * seg_t1
            seg_x2 = x1 + (x2 - x1) * seg_t2
            seg_y2 = y1 + (y2 - y1) * seg_t2
            
            # Offset sinusoidal untuk efek organik
            mid_t = (seg_t1 + seg_t2) / 2
            offset_magnitude = 0.8 * (1.0 - t1)
            offset_angle = (i + seg) * 0.5
            
            offset_x = offset_magnitude * np.sin(mid_t * np.pi * 4 + offset_angle)
            offset_y = offset_magnitude * np.cos(mid_t * np.pi * 4 + offset_angle)
            
            # Gambar segmen garis
            seg_line_x = [seg_x1 + offset_x * seg_t1, seg_x2 + offset_x * seg_t2]
            seg_line_y = [seg_y1 + offset_y * seg_t1, seg_y2 + offset_y * seg_t2]
            
            ax.plot(seg_line_x, seg_line_y, color="black", linewidth=0.4, alpha=0.5)
    
    # Layer 3: Poligon konsentris di pusat
    n_concentric = 8
    for i in range(n_concentric):
        t = i / (n_concentric - 1)
        
        # Radius konsentris
        concentric_radius = 12.0 * t
        
        # Jumlah sisi meningkat dari pusat ke luar
        concentric_sides = 3 + int(7 * t)
        
        # Rotasi meningkat
        concentric_rotation = i * 0.4
        
        # Gambar poligon konsentris
        x_con, y_con = draw_polygon(center_x, center_y, concentric_radius, 
                                   concentric_sides, concentric_rotation)
        
        lw = 0.8 + 0.8 * t
        alpha = 0.7 + 0.2 * t
        
        ax.plot(x_con, y_con, color="black", linewidth=lw, alpha=alpha)
        
        # Update bounding box
        min_x, max_x = min(min_x, x_con.min()), max(max_x, x_con.max())
        min_y, max_y = min(min_y, y_con.min()), max(max_y, y_con.max())
        
        # Hubungkan titik sudut ke spiral terdekat
        if i == n_concentric - 1:  # Poligon terluar
            for j in range(concentric_sides):
                poly_x = x_con[j]
                poly_y = y_con[j]
                
                # Cari titik spiral terdekat
                closest_dist = float("inf")
                closest_spiral = None
                
                for sx, sy, st in spiral_positions[:20]:  # Hanya spiral dalam
                    dist = np.sqrt((poly_x - sx)**2 + (poly_y - sy)**2)
                    if dist < closest_dist:
                        closest_dist = dist
                        closest_spiral = (sx, sy)
                
                if closest_spiral and closest_dist < 25:
                    sx, sy = closest_spiral
                    
                    # Gambar garis penghubung dengan kurva
                    n_curve = 15
                    t_curve = np.linspace(0, 1, n_curve)
                    
                    # Kurva Bezier dengan kontrol point di tengah
                    mid_x = (poly_x + sx) / 2 + np.random.uniform(-3, 3)
                    mid_y = (poly_y + sy) / 2 + np.random.uniform(-3, 3)
                    
                    curve_x = (1-t_curve)**2 * poly_x + 2*(1-t_curve)*t_curve*mid_x + t_curve**2*sx
                    curve_y = (1-t_curve)**2 * poly_y + 2*(1-t_curve)*t_curve*mid_y + t_curve**2*sy
                    
                    ax.plot(curve_x, curve_y, color="black", linewidth=0.3, alpha=0.4)
    
    # Layer 4: Poligon kecil di antara spiral
    for i in range(0, len(spiral_positions) - 5, 3):
        x1, y1, t1 = spiral_positions[i]
        x2, y2, t2 = spiral_positions[i + 2]
        x3, y3, t3 = spiral_positions[i + 4]
        
        # Posisi tengah antara tiga titik spiral
        mid_x = (x1 + x2 + x3) / 3
        mid_y = (y1 + y2 + y3) / 3
        
        # Ukuran berdasarkan jarak dari pusat
        center_dist = np.sqrt((mid_x - center_x)**2 + (mid_y - center_y)**2)
        small_size = 1.0 + 2.0 * (center_dist / 40)
        
        # Poligon kecil (segitiga atau segiempat)
        small_sides = 3 if i % 2 == 0 else 4
        small_rotation = i * 0.2
        
        x_small, y_small = draw_polygon(mid_x, mid_y, small_size, small_sides, small_rotation)
        
        ax.plot(x_small, y_small, color="black", linewidth=0.5, alpha=0.6)
        
        # Update bounding box
        min_x, max_x = min(min_x, x_small.min()), max(max_x, x_small.max())
        min_y, max_y = min(min_y, y_small.min()), max(max_y, y_small.max())
        
        # Hubungkan ke titik spiral terdekat
        for sx, sy, st in [(x1, y1, t1), (x2, y2, t2), (x3, y3, t3)]:
            if np.sqrt((mid_x - sx)**2 + (mid_y - sy)**2) < 15:
                ax.plot([mid_x, sx], [mid_y, sy], color="black", 
                       linewidth=0.2, alpha=0.3)
    
    # Layer 5: Elemen spiral sekunder
    secondary_center_x, secondary_center_y = center_x + 15, center_y - 12
    n_secondary = 40
    
    for i in range(n_secondary):
        t = i / n_secondary
        angle = t * 3 * 2 * np.pi
        radius = 1.5 + 8.0 * (t ** 1.5)
        
        sec_x = secondary_center_x + radius * np.cos(angle)
        sec_y = secondary_center_y + radius * np.sin(angle)
        
        # Poligon kecil di spiral sekunder
        sec_sides = 3 + int(3 * np.sin(t * np.pi))
        sec_size = 0.4 + 1.2 * t
        sec_rotation = angle * 1.2
        
        x_sec, y_sec = draw_polygon(sec_x, sec_y, sec_size, sec_sides, sec_rotation)
        
        ax.plot(x_sec, y_sec, color="black", linewidth=0.4, alpha=0.5)
        
        # Update bounding box
        min_x, max_x = min(min_x, x_sec.min()), max(max_x, x_sec.max())
        min_y, max_y = min(min_y, y_sec.min()), max(max_y, y_sec.max())
    
    # Framing dinamis
    cx_final = (min_x + max_x) / 2.0
    cy_final = (min_y + max_y) / 2.0
    w = max_x - min_x
    h = max_y - min_y
    pad = max(w, h) / 2.0 + 2.0
    
    ax.set_xlim(cx_final - pad, cx_final + pad)
    ax.set_ylim(cy_final - pad, cy_final + pad)
    
    save(fig, "spiral polygon fusion")


if __name__ == "__main__":
    spiral_polygon_fusion()