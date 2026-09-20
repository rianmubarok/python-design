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


def draw_diamond_grid(ax, cx, cy, grid_size, cell_size, rotation=0):
    """Menggambar grid berlian (diamond) dengan rotasi."""
    half_cell = cell_size / 2
    
    for i in range(-grid_size, grid_size + 1):
        for j in range(-grid_size, grid_size + 1):
            # Posisi pusat berlian
            diamond_cx = cx + (i * cell_size + j * half_cell)
            diamond_cy = cy + (j * cell_size * 0.866)  # Faktor hexagonal
            
            # Titik berlian
            points = [
                (diamond_cx, diamond_cy + half_cell),
                (diamond_cx + half_cell, diamond_cy),
                (diamond_cx, diamond_cy - half_cell),
                (diamond_cx - half_cell, diamond_cy),
                (diamond_cx, diamond_cy + half_cell)
            ]
            
            # Terapkan rotasi
            rotated_points = []
            for px, py in points:
                dx = px - cx
                dy = py - cy
                rx = dx * np.cos(rotation) - dy * np.sin(rotation)
                ry = dx * np.sin(rotation) + dy * np.cos(rotation)
                rotated_points.append((cx + rx, cy + ry))
            
            x_pts = [p[0] for p in rotated_points]
            y_pts = [p[1] for p in rotated_points]
            
            ax.plot(x_pts, y_pts, color="black", linewidth=0.7, alpha=0.5)
    
    return grid_size * cell_size * 1.5  # Return approximate radius


def circle_packing_grid_fusion():
    """Fusi circle packing dengan grid geometri berlian."""
    fig, ax = setup_ax()
    
    center_x, center_y = 50, 50
    
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    
    # Layer 1: Grid berlian dasar
    grid_radius = draw_diamond_grid(ax, center_x, center_y, 6, 5.0, rotation=0.2)
    
    # Layer 2: Circle packing di atas grid
    # Generate points dengan distribusi yang mengikuti grid berlian
    all_points = []
    
    # Titik di persimpangan grid
    for i in range(-8, 9):
        for j in range(-8, 9):
            base_x = center_x + i * 4.5
            base_y = center_y + j * 4.5
            
            # Tambahkan variasi posisi mengikuti pola berlian
            if (i + j) % 2 == 0:
                offset_x = np.random.uniform(-1.2, 1.2)
                offset_y = np.random.uniform(-1.2, 1.2)
            else:
                offset_x = np.random.uniform(-0.8, 0.8)
                offset_y = np.random.uniform(-0.8, 0.8)
            
            all_points.append([base_x + offset_x, base_y + offset_y])
    
    # Titik tambahan untuk kepadatan
    for _ in range(80):
        angle = np.random.uniform(0, 2*np.pi)
        radius = np.random.uniform(5, grid_radius * 0.8)
        x = center_x + radius * np.cos(angle)
        y = center_y + radius * np.sin(angle)
        all_points.append([x, y])
    
    points = np.array(all_points)
    
    # Filter untuk jarak minimum
    valid_points = []
    min_dist_threshold = 4.0
    
    for pt in points:
        if not valid_points:
            valid_points.append(pt)
        else:
            dists = [np.linalg.norm(pt - p) for p in valid_points]
            if min(dists) >= min_dist_threshold:
                valid_points.append(pt)
    
    points = np.array(valid_points)
    n_points = len(points)
    
    # Tambahkan titik pembatas untuk Voronoi
    grid_bounds = np.array([
        [-30, -30], [130, -30], [130, 130], [-30, 130],
        [50, -30], [130, 50], [50, 130], [-30, 50]
    ])
    all_points_for_voronoi = np.vstack([points, grid_bounds])
    vor = Voronoi(all_points_for_voronoi)
    
    # Layer 3: Gambar garis Voronoi dengan gaya yang mengikuti grid
    for simplex in vor.ridge_vertices:
        if -1 not in simplex:
            p1 = vor.vertices[simplex[0]]
            p2 = vor.vertices[simplex[1]]
            if (-20 <= p1[0] <= 120 and -20 <= p1[1] <= 120 and
                -20 <= p2[0] <= 120 and -20 <= p2[1] <= 120):
                
                # Ketebalan berdasarkan jarak dari pusat
                center_dist1 = np.sqrt((p1[0] - center_x)**2 + (p1[1] - center_y)**2)
                center_dist2 = np.sqrt((p2[0] - center_x)**2 + (p2[1] - center_y)**2)
                avg_dist = (center_dist1 + center_dist2) / 2
                
                lw = 0.5 + 0.6 * (1.0 - avg_dist / 50)
                alpha = 0.4 + 0.3 * (1.0 - avg_dist / 50)
                
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                       color="black", linewidth=lw, alpha=alpha, 
                       linestyle=(0, (3, 2)), zorder=2)
    
    # Layer 4: Circle packing dengan variasi berdasarkan grid
    radii = np.zeros(n_points)
    for i in range(n_points):
        cx, cy = points[i]
        
        # Jarak ke titik tetangga terdekat
        dists = [np.linalg.norm(points[i] - points[j]) for j in range(n_points) if i != j]
        r_neighbor = min(dists) * 0.42
        
        # Radius berdasarkan posisi dalam grid
        grid_x_dist = abs(cx - center_x)
        grid_y_dist = abs(cy - center_y)
        grid_factor = max(grid_x_dist, grid_y_dist) / 40
        
        # Radius lebih kecil di dekat pusat, lebih besar di tepi
        base_radius = max(1.2, r_neighbor * (0.9 + 0.2 * grid_factor))
        radii[i] = base_radius
    
    # Gambar lingkaran dengan gaya yang berbeda
    t = np.linspace(0, 2 * np.pi, 100)
    for i in range(n_points):
        cx, cy = points[i]
        r = radii[i]
        
        # Tentukan gaya berdasarkan posisi
        center_dist = np.sqrt((cx - center_x)**2 + (cy - center_y)**2)
        
        if center_dist < 20:
            # Lingkaran dalam: garis solid tebal
            x_circ = cx + r * np.cos(t)
            y_circ = cy + r * np.sin(t)
            lw = 1.4
            alpha = 0.9
            ax.plot(x_circ, y_circ, color="black", linewidth=lw, 
                    solid_capstyle="round", zorder=3, alpha=alpha)
            
            # Titik pusat untuk lingkaran dalam
            ax.plot(cx, cy, marker="o", markersize=1.2, 
                    color="black", zorder=4, alpha=0.8)
        elif center_dist < 40:
            # Lingkaran tengah: garis putus-putus
            x_circ = cx + r * np.cos(t)
            y_circ = cy + r * np.sin(t)
            lw = 1.0
            alpha = 0.7
            ax.plot(x_circ, y_circ, color="black", linewidth=lw, 
                    linestyle=(0, (4, 2)), zorder=3, alpha=alpha)
        else:
            # Lingkaran luar: garis tipis dengan titik
            x_circ = cx + r * np.cos(t)
            y_circ = cy + r * np.sin(t)
            lw = 0.6
            alpha = 0.5
            ax.plot(x_circ, y_circ, color="black", linewidth=lw, 
                    zorder=3, alpha=alpha)
            
            # Titik di sekeliling lingkaran luar
            for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
                marker_x = cx + r * np.cos(angle)
                marker_y = cy + r * np.sin(angle)
                ax.plot(marker_x, marker_y, marker="o", markersize=0.6, 
                        color="black", zorder=4, alpha=0.6)
        
        # Update bounding box
        x_circ = cx + r * np.cos(t)
        y_circ = cy + r * np.sin(t)
        min_x, max_x = min(min_x, x_circ.min()), max(max_x, x_circ.max())
        min_y, max_y = min(min_y, y_circ.min()), max(max_y, y_circ.max())
    
    # Layer 5: Elemen penghubung antara circle packing dan grid
    for i in range(0, n_points, 3):  # Setiap titik ketiga
        cx, cy = points[i]
        r = radii[i]
        
        # Cari titik grid terdekat (dalam bentuk grid berlian)
        grid_x = round((cx - center_x) / 4.5) * 4.5 + center_x
        grid_y = round((cy - center_y) / 4.5) * 4.5 + center_y
        
        # Gambar garis penghubung jika cukup dekat
        dist_to_grid = np.sqrt((cx - grid_x)**2 + (cy - grid_y)**2)
        if dist_to_grid < 15:
            # Garis penghubung dengan pola
            n_connect = 10
            t_connect = np.linspace(0, 1, n_connect)
            
            # Kurva Bezier kuadratik
            control_x = (cx + grid_x) / 2 + np.random.uniform(-2, 2)
            control_y = (cy + grid_y) / 2 + np.random.uniform(-2, 2)
            
            connect_x = (1-t_connect)**2 * cx + 2*(1-t_connect)*t_connect*control_x + t_connect**2*grid_x
            connect_y = (1-t_connect)**2 * cy + 2*(1-t_connect)*t_connect*control_y + t_connect**2*grid_y
            
            ax.plot(connect_x, connect_y, color="black", linewidth=0.4, alpha=0.4)
    
    # Framing dinamis
    cx_final = (min_x + max_x) / 2.0
    cy_final = (min_y + max_y) / 2.0
    w = max_x - min_x
    h = max_y - min_y
    pad = max(w, h) / 2.0 + 3.0
    
    ax.set_xlim(cx_final - pad, cx_final + pad)
    ax.set_ylim(cy_final - pad, cy_final + pad)
    
    save(fig, "circle packing grid fusion")


if __name__ == "__main__":
    circle_packing_grid_fusion()