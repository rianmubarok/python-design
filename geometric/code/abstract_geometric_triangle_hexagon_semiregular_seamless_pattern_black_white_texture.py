from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
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


def draw_triangle(cx, cy, size, rotation=0):
    """Menggambar segitiga sama sisi."""
    angles = np.array([0, 2*np.pi/3, 4*np.pi/3]) + rotation
    x = cx + size * np.cos(angles)
    y = cy + size * np.sin(angles)
    # Tutup segitiga
    x = np.append(x, x[0])
    y = np.append(y, y[0])
    return x, y


def draw_hexagon(cx, cy, size, rotation=0):
    """Menggambar heksagon beraturan."""
    angles = np.linspace(0, 2*np.pi, 7) + rotation  # 6 sisi + penutup
    x = cx + size * np.cos(angles)
    y = cy + size * np.sin(angles)
    return x, y


def triangle_hexagon_semiregular_seamless():
    """Teselasi semiregular segitiga-heksagon (3.6.3.6) yang seamless."""
    fig, ax = setup_ax()
    
    # Parameter tiling
    triangle_size = 4.0  # Radius segitiga
    hexagon_size = triangle_size * 2 / np.sqrt(3)  # Radius heksagon untuk pas
    
    # Jarak unit untuk tiling
    unit_x = triangle_size * 3
    unit_y = triangle_size * np.sqrt(3)
    
    # Jumlah unit untuk coverage
    n_units_x = 6
    n_units_y = 6
    
    # Pusat pattern
    center_x, center_y = 50, 50
    
    # Hitung offset untuk memusatkan
    offset_x = center_x - (n_units_x * unit_x) / 2
    offset_y = center_y - (n_units_y * unit_y) / 2
    
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    
    # Gambar pattern untuk setiap unit
    for ux in range(n_units_x + 1):  # +1 untuk coverage seamless
        for uy in range(n_units_y + 1):
            base_x = offset_x + ux * unit_x
            base_y = offset_y + uy * unit_y
            
            # Unit pattern dasar: segitiga dan heksagon
            # Pattern 3.6.3.6: segitiga-heksagon-segitiga-heksagon
            
            # Heksagon di pusat unit
            hex_cx = base_x + unit_x / 2
            hex_cy = base_y + unit_y / 2
            
            x_hex, y_hex = draw_hexagon(hex_cx, hex_cy, hexagon_size, rotation=np.pi/6)
            ax.plot(x_hex, y_hex, color="black", linewidth=1.2, solid_capstyle="round")
            
            # Update bounding box
            min_x, max_x = min(min_x, x_hex.min()), max(max_x, x_hex.max())
            min_y, max_y = min(min_y, y_hex.min()), max(max_y, y_hex.max())
            
            # Segitiga di sekitar heksagon
            for i in range(6):
                angle = i * np.pi / 3 + np.pi/6
                tri_cx = hex_cx + hexagon_size * 1.5 * np.cos(angle)
                tri_cy = hex_cy + hexagon_size * 1.5 * np.sin(angle)
                
                x_tri, y_tri = draw_triangle(tri_cx, tri_cy, triangle_size, rotation=angle)
                ax.plot(x_tri, y_tri, color="black", linewidth=1.0, solid_capstyle="round")
                
                # Update bounding box
                min_x, max_x = min(min_x, x_tri.min()), max(max_x, x_tri.max())
                min_y, max_y = min(min_y, y_tri.min()), max(max_y, y_tri.max())
            
            # Heksagon kecil di sudut
            for i in range(6):
                angle = i * np.pi / 3
                small_hex_cx = hex_cx + hexagon_size * np.sqrt(3) * np.cos(angle)
                small_hex_cy = hex_cy + hexagon_size * np.sqrt(3) * np.sin(angle)
                
                x_small_hex, y_small_hex = draw_hexagon(small_hex_cx, small_hex_cy, 
                                                       hexagon_size/2, rotation=angle)
                ax.plot(x_small_hex, y_small_hex, color="black", linewidth=0.8, 
                       solid_capstyle="round", alpha=0.8)
                
                # Update bounding box
                min_x, max_x = min(min_x, x_small_hex.min()), max(max_x, x_small_hex.max())
                min_y, max_y = min(min_y, y_small_hex.min()), max(max_y, y_small_hex.max())
    
    # Gambar continuation lines untuk menunjukkan seamless nature
    # Garis batas tiling
    for ux in range(n_units_x + 1):
        x_line = offset_x + ux * unit_x
        ax.axvline(x=x_line, color="gray", linewidth=0.4, alpha=0.3, linestyle="--")
    
    for uy in range(n_units_y + 1):
        y_line = offset_y + uy * unit_y
        ax.axhline(y=y_line, color="gray", linewidth=0.4, alpha=0.3, linestyle="--")
    
    # Tunjukkan unit tile dasar
    tile_width = unit_x * 2  # 2 unit untuk pattern lengkap
    tile_height = unit_y * 2
    
    # Rectangle untuk menunjukkan repeat unit
    tile_rect = plt.Rectangle((center_x - tile_width/2, center_y - tile_height/2),
                             tile_width, tile_height,
                             fill=False, linewidth=1.5, edgecolor="blue", 
                             alpha=0.6, linestyle="-")
    ax.add_patch(tile_rect)
    
    # Label repeat unit
    ax.text(center_x, center_y - tile_height/2 - 3, 
           "Seamless Repeat Unit", ha="center", va="top",
           fontsize=10, alpha=0.8, color="blue", weight="bold")
    
    # Gambar pattern continuation di luar batas untuk menunjukkan seamless
    # Continuation kiri
    cont_x = offset_x - unit_x
    for uy in range(n_units_y + 1):
        base_y = offset_y + uy * unit_y
        
        # Gambar sebagian pattern untuk menunjukkan continuity
        hex_cx = cont_x + unit_x / 2
        hex_cy = base_y + unit_y / 2
        
        x_hex, y_hex = draw_hexagon(hex_cx, hex_cy, hexagon_size, rotation=np.pi/6)
        # Filter hanya bagian yang terlihat
        mask = x_hex >= offset_x - 5
        if mask.any():
            ax.plot(x_hex[mask], y_hex[mask], color="black", linewidth=0.7, 
                   alpha=0.5, linestyle=":")
    
    # Continuation kanan
    cont_x = offset_x + (n_units_x + 1) * unit_x
    for uy in range(n_units_y + 1):
        base_y = offset_y + uy * unit_y
        
        hex_cx = cont_x + unit_x / 2
        hex_cy = base_y + unit_y / 2
        
        x_hex, y_hex = draw_hexagon(hex_cx, hex_cy, hexagon_size, rotation=np.pi/6)
        mask = x_hex <= offset_x + n_units_x * unit_x + 5
        if mask.any():
            ax.plot(x_hex[mask], y_hex[mask], color="black", linewidth=0.7, 
                   alpha=0.5, linestyle=":")
    
    # Continuation atas
    cont_y = offset_y - unit_y
    for ux in range(n_units_x + 1):
        base_x = offset_x + ux * unit_x
        
        hex_cx = base_x + unit_x / 2
        hex_cy = cont_y + unit_y / 2
        
        x_hex, y_hex = draw_hexagon(hex_cx, hex_cy, hexagon_size, rotation=np.pi/6)
        mask = y_hex >= offset_y - 5
        if mask.any():
            ax.plot(x_hex[mask], y_hex[mask], color="black", linewidth=0.7, 
                   alpha=0.5, linestyle=":")
    
    # Continuation bawah
    cont_y = offset_y + (n_units_y + 1) * unit_y
    for ux in range(n_units_x + 1):
        base_x = offset_x + ux * unit_x
        
        hex_cx = base_x + unit_x / 2
        hex_cy = cont_y + unit_y / 2
        
        x_hex, y_hex = draw_hexagon(hex_cx, hex_cy, hexagon_size, rotation=np.pi/6)
        mask = y_hex <= offset_y + n_units_y * unit_y + 5
        if mask.any():
            ax.plot(x_hex[mask], y_hex[mask], color="black", linewidth=0.7, 
                   alpha=0.5, linestyle=":")
    
    # Diagram showing how tiles connect
    # Draw arrows between tiles
    arrow_start_x = center_x - tile_width/4
    arrow_end_x = center_x + tile_width/4
    arrow_y = center_y + tile_height/2 + 8
    
    ax.annotate("", xy=(arrow_end_x, arrow_y), xytext=(arrow_start_x, arrow_y),
               arrowprops=dict(arrowstyle="<->", color="green", lw=1.5, alpha=0.7))
    
    ax.text(center_x, arrow_y + 2, "Tile Connection", ha="center", va="bottom",
           fontsize=9, alpha=0.7, color="green")
    
    # Framing untuk fokus pada area seamless
    display_pad = 8.0
    ax.set_xlim(center_x - tile_width/2 - display_pad, 
                center_x + tile_width/2 + display_pad)
    ax.set_ylim(center_y - tile_height/2 - display_pad,
                center_y + tile_height/2 + display_pad)
    
    save(fig, "triangle hexagon semiregular seamless")


if __name__ == "__main__":
    triangle_hexagon_semiregular_seamless()