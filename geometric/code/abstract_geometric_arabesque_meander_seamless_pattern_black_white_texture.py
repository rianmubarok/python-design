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


def draw_greek_key_unit(cx, cy, size, rotation=0):
    """Menggambar unit Greek key/meander pattern."""
    # Greek key pattern: bentuk persegi dengan tikungan
    unit_points = []
    
    # Ukuran relatif
    s = size
    h = s / 2
    
    # Titik-titik untuk Greek key pattern
    # Bentuk dasar: ┏┓
    #              ┗┛
    base_points = [
        (-h, -h), (-h, h), (0, h), (0, 0),
        (h, 0), (h, -h), (0, -h), (0, 0),
        (-h, 0), (-h, -h)  # Kembali ke awal
    ]
    
    # Terapkan rotasi
    cos_r = np.cos(rotation)
    sin_r = np.sin(rotation)
    
    for px, py in base_points:
        rx = px * cos_r - py * sin_r
        ry = px * sin_r + py * cos_r
        unit_points.append((cx + rx, cy + ry))
    
    return unit_points


def draw_arabesque_curve(cx, cy, size, direction=1):
    """Menggambar kurva arabesque."""
    # Kurva sinusoidal dengan modifikasi
    n_points = 50
    t = np.linspace(0, 2*np.pi, n_points)
    
    # Kurva dengan multiple harmonics untuk efek arabesque
    x_curve = cx + size * (np.cos(t) + 0.3 * np.cos(3*t) * direction)
    y_curve = cy + size * (np.sin(t) + 0.2 * np.sin(2*t) * direction)
    
    return x_curve, y_curve


def arabesque_meander_seamless():
    """Pattern arabesque dan Greek key meander yang seamless."""
    fig, ax = setup_ax()
    
    center_x, center_y = 50, 50
    
    # Parameter tiling
    unit_size = 6.0
    tile_width = unit_size * 4
    tile_height = unit_size * 4
    
    # Jumlah tiles
    n_tiles_x = 4
    n_tiles_y = 4
    
    # Hitung offset untuk memusatkan
    offset_x = center_x - (n_tiles_x * tile_width) / 2
    offset_y = center_y - (n_tiles_y * tile_height) / 2
    
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    
    # Layer 1: Greek key meander grid
    for tx in range(n_tiles_x):
        for ty in range(n_tiles_y):
            tile_cx = offset_x + tx * tile_width + tile_width/2
            tile_cy = offset_y + ty * tile_height + tile_height/2
            
            # Gambar Greek key di setiap sudut tile
            for corner in range(4):
                corner_angle = corner * np.pi/2
                corner_x = tile_cx + (tile_width/2 - unit_size) * np.cos(corner_angle)
                corner_y = tile_cy + (tile_height/2 - unit_size) * np.sin(corner_angle)
                
                greek_points = draw_greek_key_unit(corner_x, corner_y, 
                                                  unit_size, corner_angle)
                
                x_greek = [p[0] for p in greek_points]
                y_greek = [p[1] for p in greek_points]
                
                ax.plot(x_greek, y_greek, color="black", linewidth=1.2, 
                       solid_capstyle="round")
                
                # Update bounding box
                min_x, max_x = min(min_x, min(x_greek)), max(max_x, max(x_greek))
                min_y, max_y = min(min_y, min(y_greek)), max(max_y, max(y_greek))
            
            # Gambar Greek key di tengah sisi tile
            for side in range(4):
                side_angle = side * np.pi/2
                side_x = tile_cx + (tile_width/2 - unit_size/2) * np.cos(side_angle)
                side_y = tile_cy + (tile_height/2 - unit_size/2) * np.sin(side_angle)
                
                side_points = draw_greek_key_unit(side_x, side_y, 
                                                 unit_size/1.5, side_angle + np.pi/4)
                
                x_side = [p[0] for p in side_points]
                y_side = [p[1] for p in side_points]
                
                ax.plot(x_side, y_side, color="black", linewidth=0.9, 
                       solid_capstyle="round", alpha=0.8)
                
                # Update bounding box
                min_x, max_x = min(min_x, min(x_side)), max(max_x, max(x_side))
                min_y, max_y = min(min_y, min(y_side)), max(max_y, max(y_side))
    
    # Layer 2: Arabesque curves connecting the meanders
    for tx in range(n_tiles_x):
        for ty in range(n_tiles_y):
            tile_cx = offset_x + tx * tile_width + tile_width/2
            tile_cy = offset_y + ty * tile_height + tile_height/2
            
            # Arabesque di pusat tile
            arabesque_size = unit_size * 1.5
            
            for direction in [1, -1]:
                x_arab, y_arab = draw_arabesque_curve(tile_cx, tile_cy, 
                                                     arabesque_size, direction)
                
                ax.plot(x_arab, y_arab, color="black", linewidth=0.8, 
                       solid_capstyle="round", alpha=0.7)
                
                # Update bounding box
                min_x, max_x = min(min_x, min(x_arab)), max(max_x, max(x_arab))
                min_y, max_y = min(min_y, min(y_arab)), max(max_y, max(y_arab))
            
            # Arabesque kecil di antara Greek keys
            for i in range(4):
                angle = i * np.pi/2 + np.pi/4
                small_x = tile_cx + (tile_width/3) * np.cos(angle)
                small_y = tile_cy + (tile_height/3) * np.sin(angle)
                
                x_small, y_small = draw_arabesque_curve(small_x, small_y, 
                                                       unit_size/2, (-1)**i)
                
                ax.plot(x_small, y_small, color="black", linewidth=0.6, 
                       solid_capstyle="round", alpha=0.6)
                
                # Update bounding box
                min_x, max_x = min(min_x, min(x_small)), max(max_x, max(x_small))
                min_y, max_y = min(min_y, min(y_small)), max(max_y, max(y_small))
    
    # Layer 3: Connecting lines untuk seamless effect
    # Garis penghubung antara tiles
    for tx in range(n_tiles_x + 1):
        x_conn = offset_x + tx * tile_width
        for ty in range(n_tiles_y):
            y_start = offset_y + ty * tile_height + tile_height/2
            
            # Garis vertikal penghubung
            if tx < n_tiles_x:  # Garis di dalam area
                ax.plot([x_conn, x_conn], [y_start - unit_size, y_start + unit_size],
                       color="black", linewidth=0.7, alpha=0.5)
            else:  # Garis di batas kanan (untuk menunjukkan continuity)
                ax.plot([x_conn, x_conn + 2], [y_start - unit_size, y_start + unit_size],
                       color="black", linewidth=0.5, alpha=0.3, linestyle=":")
    
    for ty in range(n_tiles_y + 1):
        y_conn = offset_y + ty * tile_height
        for tx in range(n_tiles_x):
            x_start = offset_x + tx * tile_width + tile_width/2
            
            # Garis horizontal penghubung
            if ty < n_tiles_y:  # Garis di dalam area
                ax.plot([x_start - unit_size, x_start + unit_size], [y_conn, y_conn],
                       color="black", linewidth=0.7, alpha=0.5)
            else:  # Garis di batas bawah
                ax.plot([x_start - unit_size, x_start + unit_size], [y_conn, y_conn + 2],
                       color="black", linewidth=0.5, alpha=0.3, linestyle=":")
    
    # Layer 4: Decorative elements untuk menunjukkan seamless connections
    # Pattern continuation di luar batas
    continuation_dist = 5.0
    
    # Continuation kiri
    left_x = offset_x - continuation_dist
    for ty in range(n_tiles_y):
        tile_cy = offset_y + ty * tile_height + tile_height/2
        
        # Gambar sebagian pattern
        x_arab, y_arab = draw_arabesque_curve(left_x, tile_cy, unit_size, 1)
        mask = x_arab >= offset_x - 2
        if mask.any():
            ax.plot(x_arab[mask], y_arab[mask], color="black", linewidth=0.5, 
                   alpha=0.3, linestyle="--")
    
    # Continuation kanan
    right_x = offset_x + n_tiles_x * tile_width + continuation_dist
    for ty in range(n_tiles_y):
        tile_cy = offset_y + ty * tile_height + tile_height/2
        
        x_arab, y_arab = draw_arabesque_curve(right_x, tile_cy, unit_size, -1)
        mask = x_arab <= offset_x + n_tiles_x * tile_width + 2
        if mask.any():
            ax.plot(x_arab[mask], y_arab[mask], color="black", linewidth=0.5, 
                   alpha=0.3, linestyle="--")
    
    # Continuation atas
    top_y = offset_y - continuation_dist
    for tx in range(n_tiles_x):
        tile_cx = offset_x + tx * tile_width + tile_width/2
        
        x_arab, y_arab = draw_arabesque_curve(tile_cx, top_y, unit_size, 1)
        mask = y_arab >= offset_y - 2
        if mask.any():
            ax.plot(x_arab[mask], y_arab[mask], color="black", linewidth=0.5, 
                   alpha=0.3, linestyle="--")
    
    # Continuation bawah
    bottom_y = offset_y + n_tiles_y * tile_height + continuation_dist
    for tx in range(n_tiles_x):
        tile_cx = offset_x + tx * tile_width + tile_width/2
        
        x_arab, y_arab = draw_arabesque_curve(tile_cx, bottom_y, unit_size, -1)
        mask = y_arab <= offset_y + n_tiles_y * tile_height + 2
        if mask.any():
            ax.plot(x_arab[mask], y_arab[mask], color="black", linewidth=0.5, 
                   alpha=0.3, linestyle="--")
    
    # Tunjukkan repeat unit dengan rectangle
    repeat_rect = plt.Rectangle((center_x - tile_width, center_y - tile_height),
                               tile_width * 2, tile_height * 2,
                               fill=False, linewidth=2, edgecolor="purple", 
                               alpha=0.7, linestyle="-")
    ax.add_patch(repeat_rect)
    
    # Label repeat unit
    ax.text(center_x, center_y - tile_height - 4, 
           "Seamless Repeat Unit (2×2 Tiles)", ha="center", va="top",
           fontsize=11, alpha=0.8, color="purple", weight="bold")
    
    # Tunjukkan how tiles connect dengan arrows
    # Horizontal connection
    arrow_h_start = center_x - tile_width
    arrow_h_end = center_x + tile_width
    arrow_h_y = center_y + tile_height + 6
    
    ax.annotate("", xy=(arrow_h_end, arrow_h_y), xytext=(arrow_h_start, arrow_h_y),
               arrowprops=dict(arrowstyle="<->", color="orange", lw=1.5, alpha=0.7))
    
    ax.text(center_x, arrow_h_y + 2, "Horizontal Repeat", ha="center", va="bottom",
           fontsize=9, alpha=0.7, color="orange")
    
    # Vertical connection
    arrow_v_x = center_x + tile_width + 6
    arrow_v_start = center_y - tile_height
    arrow_v_end = center_y + tile_height
    
    ax.annotate("", xy=(arrow_v_x, arrow_v_end), xytext=(arrow_v_x, arrow_v_start),
               arrowprops=dict(arrowstyle="<->", color="orange", lw=1.5, alpha=0.7))
    
    ax.text(arrow_v_x + 4, center_y, "Vertical Repeat", ha="left", va="center",
           fontsize=9, alpha=0.7, color="orange", rotation=90)
    
    # Framing untuk fokus pada area seamless
    display_pad = 10.0
    ax.set_xlim(center_x - tile_width - display_pad, 
                center_x + tile_width + display_pad)
    ax.set_ylim(center_y - tile_height - display_pad,
                center_y + tile_height + display_pad)
    
    save(fig, "arabesque meander seamless")


if __name__ == "__main__":
    arabesque_meander_seamless()