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
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
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


def rotate_point(x, y, cx, cy, angle):
    """Menerapkan rotasi 2D pada titik (x, y) terhadap pusat (cx, cy)."""
    tx, ty = x - cx, y - cy
    rx = tx * np.cos(angle) - ty * np.sin(angle)
    ry = tx * np.sin(angle) + ty * np.cos(angle)
    return cx + rx, cy + ry


def draw_islamic_star(cx, cy, outer_radius, inner_radius, n_points=8):
    """Menggambar bintang islamic dengan n titik."""
    angles = []
    radii = []
    
    for i in range(n_points * 2):  # n_points × 2 (outer/inner)
        angle = i * np.pi / n_points
        if i % 2 == 0:
            radius = outer_radius
        else:
            radius = inner_radius
        angles.append(angle)
        radii.append(radius)
    
    # Tutup bentuk
    angles.append(angles[0])
    radii.append(radii[0])
    
    x = [cx + r * np.cos(a) for r, a in zip(radii, angles)]
    y = [cy + r * np.sin(a) for r, a in zip(radii, angles)]
    
    return x, y


def draw_kaleidoscope_triangle(cx, cy, base_radius, height, rotation=0):
    """Menggambar segitiga untuk pola kaleidoskop."""
    # Titik segitiga (pusat di puncak)
    points = np.array([
        [cx, cy + height],
        [cx - base_radius/2, cy],
        [cx + base_radius/2, cy],
        [cx, cy + height]
    ])
    
    # Terapkan rotasi
    rotated_points = []
    for x, y in points:
        rx, ry = rotate_point(x, y, cx, cy, rotation)
        rotated_points.append([rx, ry])
    
    return np.array(rotated_points)


def arabesque_kaleidoscope_fusion():
    """Fusi pola arabesque islamic dengan simetri kaleidoskop."""
    fig, ax = setup_ax()
    
    center_x, center_y = 50, 50
    n_symmetry = 12  # Simetri 12-lipat
    
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    
    # Layer 1: Pola islamic di pusat dengan simetri kaleidoskop
    islamic_radius = 35
    for i in range(n_symmetry):
        angle = i * 2 * np.pi / n_symmetry
        
        # Bintang islamic di setiap posisi simetri
        star_outer = 6.0
        star_inner = star_outer * 0.4
        
        # Posisi bintang di lingkaran
        star_cx = center_x + islamic_radius * np.cos(angle)
        star_cy = center_y + islamic_radius * np.sin(angle)
        
        # Gambar bintang dengan rotasi sesuai posisi
        x_star, y_star = draw_islamic_star(star_cx, star_cy, star_outer, star_inner, 6)
        ax.plot(x_star, y_star, color="black", linewidth=1.3, solid_capstyle="round")
        
        # Hubungkan bintang dengan garis arabesque
        if i > 0:
            prev_angle = (i-1) * 2 * np.pi / n_symmetry
            prev_cx = center_x + islamic_radius * np.cos(prev_angle)
            prev_cy = center_y + islamic_radius * np.sin(prev_angle)
            
            # Garis lengkung menghubungkan bintang
            n_curve_points = 20
            t_curve = np.linspace(0, 1, n_curve_points)
            
            # Kurva Bezier sederhana
            curve_x = (1-t_curve)**2 * prev_cx + 2*(1-t_curve)*t_curve * center_x + t_curve**2 * star_cx
            curve_y = (1-t_curve)**2 * prev_cy + 2*(1-t_curve)*t_curve * center_y + t_curve**2 * star_cy
            
            ax.plot(curve_x, curve_y, color="black", linewidth=0.8, alpha=0.7)
        
        # Update bounding box
        min_x, max_x = min(min_x, min(x_star)), max(max_x, max(x_star))
        min_y, max_y = min(min_y, min(y_star)), max(max_y, max(y_star))
    
    # Layer 2: Elemen kaleidoskop di antara bintang
    kaleidoscope_radius = 20
    for i in range(n_symmetry):
        for j in range(3):  # Tiga lapisan segitiga
            base_radius = 2.5 + j * 1.5
            height = 4.0 + j * 1.2
            
            # Posisi segitiga
            triangle_angle = i * 2 * np.pi / n_symmetry + j * 0.1
            triangle_radius = kaleidoscope_radius + j * 5
            
            triangle_cx = center_x + triangle_radius * np.cos(triangle_angle)
            triangle_cy = center_y + triangle_radius * np.sin(triangle_angle)
            
            # Gambar segitiga
            triangle_points = draw_kaleidoscope_triangle(triangle_cx, triangle_cy, 
                                                        base_radius, height, 
                                                        triangle_angle)
            
            ax.plot(triangle_points[:, 0], triangle_points[:, 1], 
                   color="black", linewidth=1.0 - j*0.2, alpha=0.8)
            
            # Update bounding box
            min_x, max_x = min(min_x, triangle_points[:, 0].min()), max(max_x, triangle_points[:, 0].max())
            min_y, max_y = min(min_y, triangle_points[:, 1].min()), max(max_y, triangle_points[:, 1].max())
    
    # Layer 3: Pola islamic di pusat
    center_star_outer = 10.0
    center_star_inner = center_star_outer * 0.35
    x_center_star, y_center_star = draw_islamic_star(center_x, center_y, 
                                                    center_star_outer, center_star_inner, 8)
    ax.plot(x_center_star, y_center_star, color="black", linewidth=1.8, solid_capstyle="round")
    
    # Pola islamic sekunder di sekitar pusat
    secondary_radius = 12
    for i in range(8):
        secondary_angle = i * 2 * np.pi / 8
        secondary_cx = center_x + secondary_radius * np.cos(secondary_angle)
        secondary_cy = center_y + secondary_radius * np.sin(secondary_angle)
        
        # Pola islamic kecil
        small_outer = 2.5
        small_inner = small_outer * 0.5
        x_small, y_small = draw_islamic_star(secondary_cx, secondary_cy, 
                                           small_outer, small_inner, 4)
        
        ax.plot(x_small, y_small, color="black", linewidth=0.9, alpha=0.7)
        
        # Update bounding box
        min_x, max_x = min(min_x, min(x_small)), max(max_x, max(x_small))
        min_y, max_y = min(min_y, min(y_small)), max(max_y, max(y_small))
    
    # Layer 4: Elemen penghubung arabesque-kaleidoskop
    connecting_radius = 28
    for i in range(n_symmetry):
        angle1 = i * 2 * np.pi / n_symmetry
        angle2 = (i + 1) % n_symmetry * 2 * np.pi / n_symmetry
        
        cx1 = center_x + connecting_radius * np.cos(angle1)
        cy1 = center_y + connecting_radius * np.sin(angle1)
        cx2 = center_x + connecting_radius * np.cos(angle2)
        cy2 = center_y + connecting_radius * np.sin(angle2)
        
        # Garis penghubung dengan pola islamic
        n_connect_points = 25
        t_connect = np.linspace(0, 1, n_connect_points)
        
        # Kurva dengan multiple kontrol points untuk pola arabesque
        control1_x = center_x + (connecting_radius + 8) * np.cos((angle1 + angle2)/2)
        control1_y = center_y + (connecting_radius + 8) * np.sin((angle1 + angle2)/2)
        control2_x = center_x + (connecting_radius - 8) * np.cos((angle1 + angle2)/2 + np.pi/6)
        control2_y = center_y + (connecting_radius - 8) * np.sin((angle1 + angle2)/2 + np.pi/6)
        
        # Kurva Bezier kubik
        connect_x = (1-t_connect)**3 * cx1 + 3*(1-t_connect)**2*t_connect*control1_x + \
                   3*(1-t_connect)*t_connect**2*control2_x + t_connect**3*cx2
        connect_y = (1-t_connect)**3 * cy1 + 3*(1-t_connect)**2*t_connect*control1_y + \
                   3*(1-t_connect)*t_connect**2*control2_y + t_connect**3*cy2
        
        ax.plot(connect_x, connect_y, color="black", linewidth=0.7, alpha=0.6)
    
    # Framing dinamis
    cx_final = (min_x + max_x) / 2.0
    cy_final = (min_y + max_y) / 2.0
    w = max_x - min_x
    h = max_y - min_y
    pad = max(w, h) / 2.0 + 5.0
    
    ax.set_xlim(cx_final - pad, cx_final + pad)
    ax.set_ylim(cy_final - pad, cy_final + pad)
    
    save(fig, "arabesque kaleidoscope fusion")


if __name__ == "__main__":
    arabesque_kaleidoscope_fusion()