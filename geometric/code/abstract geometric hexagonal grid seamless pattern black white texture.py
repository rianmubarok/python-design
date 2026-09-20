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


def draw hexagon(cx, cy, size):
    """Menggambar heksagon beraturan dengan ukuran sisi."""
    angles = np.linspace(0, 2 * np.pi, 7)  # 6 sisi + penutup
    x = cx + size * np.cos(angles)
    y = cy + size * np.sin(angles)
    return x, y


def hexagonal grid seamless():
    """Grid heksagonal seamless yang dapat ditile tanpa batas."""
    fig, ax = setup ax()
    
    # Parameter grid heksagonal
    hex size = 5.0  # Radius heksagon
    hex spacing = hex size * np.sqrt(3)  # Jarak antar pusat heksagon
    
    # Hitung jumlah baris dan kolom untuk coverage penuh
    n cols = 12
    n rows = 12
    
    # Offset untuk membuat pattern seamless
    # Pusat pattern di tengah canvas
    offset x = 50.0
    offset y = 50.0
    
    # Buat grid yang lebih besar untuk memastikan coverage seamless
    extended cols = n cols + 2
    extended rows = n rows + 2
    
    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")
    
    # Gambar semua heksagon
    for row in range(extended rows):
        for col in range(extended cols):
            # Posisi pusat heksagon
            cx = offset x + col * hex spacing
            if row % 2 == 1:
                cx += hex spacing / 2.0  # Offset untuk baris ganjil
            
            cy = offset y + row * hex size * 1.5
            
            # Gambar heksagon
            x hex, y hex = draw hexagon(cx, cy, hex size)
            
            # Update bounding box
            min x, max x = min(min x, x hex.min()), max(max x, x hex.max())
            min y, max y = min(min y, y hex.min()), max(max y, y hex.max())
            
            # Ketebalan garis konsisten untuk tiling
            lw = 1.0
            
            # Gambar heksagon
            ax.plot(x hex, y hex, color="black", linewidth=lw, solid capstyle="round")
            
            # Gambar garis penghubung internal untuk efek jaring
            # Garis dari pusat ke sudut
            for i in range(6):
                angle = i * np.pi / 3
                x line = [cx, cx + hex size * np.cos(angle)]
                y line = [cy, cy + hex size * np.sin(angle)]
                ax.plot(x line, y line, color="black", linewidth=0.6, alpha=0.7)
    
    # Gambar heksagon yang dipotong untuk menunjukkan sifat seamless
    # Ini menunjukkan bagaimana pattern akan berlanjut di luar batas
    
    # Batas kiri
    for row in range(extended rows):
        cx = offset x - hex spacing
        if row % 2 == 1:
            cx += hex spacing / 2.0
        cy = offset y + row * hex size * 1.5
        
        # Hanya gambar sebagian heksagon untuk menunjukkan continuity
        x hex, y hex = draw hexagon(cx, cy, hex size)
        # Filter hanya bagian yang masuk area utama
        mask = x hex >= 0
        if mask.any():
            ax.plot(x hex[mask], y hex[mask], color="black", linewidth=0.7, alpha=0.5, linestyle="--")
    
    # Batas kanan
    for row in range(extended rows):
        cx = offset x + (extended cols - 1) * hex spacing
        if row % 2 == 1:
            cx += hex spacing / 2.0
        cy = offset y + row * hex size * 1.5
        
        x hex, y hex = draw hexagon(cx, cy, hex size)
        mask = x hex <= 100
        if mask.any():
            ax.plot(x hex[mask], y hex[mask], color="black", linewidth=0.7, alpha=0.5, linestyle="--")
    
    # Batas atas
    for col in range(extended cols):
        cx = offset x + col * hex spacing
        cy = offset y - hex size * 1.5
        
        x hex, y hex = draw hexagon(cx, cy, hex size)
        mask = y hex >= 0
        if mask.any():
            ax.plot(x hex[mask], y hex[mask], color="black", linewidth=0.7, alpha=0.5, linestyle="--")
    
    # Batas bawah
    for col in range(extended cols):
        cx = offset x + col * hex spacing
        cy = offset y + (extended rows - 1) * hex size * 1.5
        
        x hex, y hex = draw hexagon(cx, cy, hex size)
        mask = y hex <= 100
        if mask.any():
            ax.plot(x hex[mask], y hex[mask], color="black", linewidth=0.7, alpha=0.5, linestyle="--")
    
    # Tambahkan guide lines untuk menunjukkan tiling
    # Garis vertikal tiling boundaries
    for i in range(3):
        x boundary = offset x + i * hex spacing * 4
        ax.axvline(x=x boundary, color="gray", linewidth=0.3, alpha=0.3, linestyle=":")
        
        # Label untuk menunjukkan repeat unit
        if i < 2:
            ax.text(x boundary + hex spacing * 2, offset y - 10, 
                   f"Repeat Unit {i+1}", ha="center", va="center", 
                   fontsize=8, alpha=0.5, color="gray")
    
    # Garis horizontal tiling boundaries
    for i in range(3):
        y boundary = offset y + i * hex size * 1.5 * 4
        ax.axhline(y=y boundary, color="gray", linewidth=0.3, alpha=0.3, linestyle=":")
    
    # Tunjukkan area tile unit
    tile width = hex spacing * 4
    tile height = hex size * 1.5 * 4
    
    tile rect = plt.Rectangle((offset x - tile width/2, offset y - tile height/2),
                             tile width, tile height,
                             fill=False, linewidth=1, edgecolor="red", 
                             alpha=0.5, linestyle="-")
    ax.add patch(tile rect)
    
    # Label tile unit
    ax.text(offset x, offset y - tile height/2 - 2, 
           "Basic Tile Unit", ha="center", va="top",
           fontsize=9, alpha=0.7, color="red")
    
    # Framing untuk menunjukkan seamless nature
    # Crop ke area yang menunjukkan pattern lengkap
    display pad = 5.0
    ax.set xlim(offset x - tile width/2 - display pad, 
                offset x + tile width/2 + display pad)
    ax.set ylim(offset y - tile height/2 - display pad,
                offset y + tile height/2 + display pad)
    
    save(fig, "hexagonal grid seamless")


if   name   == "  main  ":
    hexagonal grid seamless()