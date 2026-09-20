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


def draw_hexagon(cx, cy, size):
    """Menggambar heksagon beraturan dengan ukuran sisi."""
    angles = np.linspace(0, 2 * np.pi, 7)  # 6 sisi + penutup
    x = cx + size * np.cos(angles)
    y = cy + size * np.sin(angles)
    return x, y


def hexagonal_grid_seamless():
    """Grid heksagonal seamless yang dapat ditile tanpa batas."""
    fig, ax = setup_ax()
    
    # Parameter grid heksagonal
    hex_size = 5.0  # Radius heksagon
    hex_spacing = hex_size * np.sqrt(3)  # Jarak antar pusat heksagon
    
    # Hitung jumlah baris dan kolom untuk coverage penuh
    n_cols = 12
    n_rows = 12
    
    # Offset untuk membuat pattern seamless
    # Pusat pattern di tengah canvas
    offset_x = 50.0
    offset_y = 50.0
    
    # Buat grid yang lebih besar untuk memastikan coverage seamless
    extended_cols = n_cols + 2
    extended_rows = n_rows + 2
    
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    
    # Gambar semua heksagon
    for row in range(extended_rows):
        for col in range(extended_cols):
            # Posisi pusat heksagon
            cx = offset_x + col * hex_spacing
            if row % 2 == 1:
                cx += hex_spacing / 2.0  # Offset untuk baris ganjil
            
            cy = offset_y + row * hex_size * 1.5
            
            # Gambar heksagon
            x_hex, y_hex = draw_hexagon(cx, cy, hex_size)
            
            # Update bounding box
            min_x, max_x = min(min_x, x_hex.min()), max(max_x, x_hex.max())
            min_y, max_y = min(min_y, y_hex.min()), max(max_y, y_hex.max())
            
            # Ketebalan garis konsisten untuk tiling
            lw = 1.0
            
            # Gambar heksagon
            ax.plot(x_hex, y_hex, color="black", linewidth=lw, solid_capstyle="round")
            
            # Gambar garis penghubung internal untuk efek jaring
            # Garis dari pusat ke sudut
            for i in range(6):
                angle = i * np.pi / 3
                x_line = [cx, cx + hex_size * np.cos(angle)]
                y_line = [cy, cy + hex_size * np.sin(angle)]
                ax.plot(x_line, y_line, color="black", linewidth=0.6, alpha=0.7)
    
    # Gambar heksagon yang dipotong untuk menunjukkan sifat seamless
    # Ini menunjukkan bagaimana pattern akan berlanjut di luar batas
    
    # Batas kiri
    for row in range(extended_rows):
        cx = offset_x - hex_spacing
        if row % 2 == 1:
            cx += hex_spacing / 2.0
        cy = offset_y + row * hex_size * 1.5
        
        # Hanya gambar sebagian heksagon untuk menunjukkan continuity
        x_hex, y_hex = draw_hexagon(cx, cy, hex_size)
        # Filter hanya bagian yang masuk area utama
        mask = x_hex >= 0
        if mask.any():
            ax.plot(x_hex[mask], y_hex[mask], color="black", linewidth=0.7, alpha=0.5, linestyle="--")
    
    # Batas kanan
    for row in range(extended_rows):
        cx = offset_x + (extended_cols - 1) * hex_spacing
        if row % 2 == 1:
            cx += hex_spacing / 2.0
        cy = offset_y + row * hex_size * 1.5
        
        x_hex, y_hex = draw_hexagon(cx, cy, hex_size)
        mask = x_hex <= 100
        if mask.any():
            ax.plot(x_hex[mask], y_hex[mask], color="black", linewidth=0.7, alpha=0.5, linestyle="--")
    
    # Batas atas
    for col in range(extended_cols):
        cx = offset_x + col * hex_spacing
        cy = offset_y - hex_size * 1.5
        
        x_hex, y_hex = draw_hexagon(cx, cy, hex_size)
        mask = y_hex >= 0
        if mask.any():
            ax.plot(x_hex[mask], y_hex[mask], color="black", linewidth=0.7, alpha=0.5, linestyle="--")
    
    # Batas bawah
    for col in range(extended_cols):
        cx = offset_x + col * hex_spacing
        cy = offset_y + (extended_rows - 1) * hex_size * 1.5
        
        x_hex, y_hex = draw_hexagon(cx, cy, hex_size)
        mask = y_hex <= 100
        if mask.any():
            ax.plot(x_hex[mask], y_hex[mask], color="black", linewidth=0.7, alpha=0.5, linestyle="--")
    
    # Tambahkan guide lines untuk menunjukkan tiling
    # Garis vertikal tiling boundaries
    for i in range(3):
        x_boundary = offset_x + i * hex_spacing * 4
        ax.axvline(x=x_boundary, color="gray", linewidth=0.3, alpha=0.3, linestyle=":")
        
        # Label untuk menunjukkan repeat unit
        if i < 2:
            ax.text(x_boundary + hex_spacing * 2, offset_y - 10, 
                   f"Repeat Unit {i+1}", ha="center", va="center", 
                   fontsize=8, alpha=0.5, color="gray")
    
    # Garis horizontal tiling boundaries
    for i in range(3):
        y_boundary = offset_y + i * hex_size * 1.5 * 4
        ax.axhline(y=y_boundary, color="gray", linewidth=0.3, alpha=0.3, linestyle=":")
    
    # Tunjukkan area tile unit
    tile_width = hex_spacing * 4
    tile_height = hex_size * 1.5 * 4
    
    tile_rect = plt.Rectangle((offset_x - tile_width/2, offset_y - tile_height/2),
                             tile_width, tile_height,
                             fill=False, linewidth=1, edgecolor="red", 
                             alpha=0.5, linestyle="-")
    ax.add_patch(tile_rect)
    
    # Label tile unit
    ax.text(offset_x, offset_y - tile_height/2 - 2, 
           "Basic Tile Unit", ha="center", va="top",
           fontsize=9, alpha=0.7, color="red")
    
    # Framing untuk menunjukkan seamless nature
    # Crop ke area yang menunjukkan pattern lengkap
    display_pad = 5.0
    ax.set_xlim(offset_x - tile_width/2 - display_pad, 
                offset_x + tile_width/2 + display_pad)
    ax.set_ylim(offset_y - tile_height/2 - display_pad,
                offset_y + tile_height/2 + display_pad)
    
    save(fig, "hexagonal grid seamless")


if __name__ == "__main__":
    hexagonal_grid_seamless()