import numpy as np
import matplotlib.pyplot as plt
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


def draw greek key unit(cx, cy, size, rotation=0):
    """Menggambar unit Greek key/meander pattern."""
    # Greek key pattern: bentuk persegi dengan tikungan
    unit points = []
    
    # Ukuran relatif
    s = size
    h = s / 2
    
    # Titik-titik untuk Greek key pattern
    # Bentuk dasar: ┏┓
    #              ┗┛
    base points = [
        (-h, -h), (-h, h), (0, h), (0, 0),
        (h, 0), (h, -h), (0, -h), (0, 0),
        (-h, 0), (-h, -h)  # Kembali ke awal
    ]
    
    # Terapkan rotasi
    cos r = np.cos(rotation)
    sin r = np.sin(rotation)
    
    for px, py in base points:
        rx = px * cos r - py * sin r
        ry = px * sin r + py * cos r
        unit points.append((cx + rx, cy + ry))
    
    return unit points


def draw arabesque curve(cx, cy, size, direction=1):
    """Menggambar kurva arabesque."""
    # Kurva sinusoidal dengan modifikasi
    n points = 50
    t = np.linspace(0, 2*np.pi, n points)
    
    # Kurva dengan multiple harmonics untuk efek arabesque
    x curve = cx + size * (np.cos(t) + 0.3 * np.cos(3*t) * direction)
    y curve = cy + size * (np.sin(t) + 0.2 * np.sin(2*t) * direction)
    
    return x curve, y curve


def arabesque meander seamless():
    """Pattern arabesque dan Greek key meander yang seamless."""
    fig, ax = setup ax()
    
    center x, center y = 50, 50
    
    # Parameter tiling
    unit size = 6.0
    tile width = unit size * 4
    tile height = unit size * 4
    
    # Jumlah tiles
    n tiles x = 4
    n tiles y = 4
    
    # Hitung offset untuk memusatkan
    offset x = center x - (n tiles x * tile width) / 2
    offset y = center y - (n tiles y * tile height) / 2
    
    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")
    
    # Layer 1: Greek key meander grid
    for tx in range(n tiles x):
        for ty in range(n tiles y):
            tile cx = offset x + tx * tile width + tile width/2
            tile cy = offset y + ty * tile height + tile height/2
            
            # Gambar Greek key di setiap sudut tile
            for corner in range(4):
                corner angle = corner * np.pi/2
                corner x = tile cx + (tile width/2 - unit size) * np.cos(corner angle)
                corner y = tile cy + (tile height/2 - unit size) * np.sin(corner angle)
                
                greek points = draw greek key unit(corner x, corner y, 
                                                  unit size, corner angle)
                
                x greek = [p[0] for p in greek points]
                y greek = [p[1] for p in greek points]
                
                ax.plot(x greek, y greek, color="black", linewidth=1.2, 
                       solid capstyle="round")
                
                # Update bounding box
                min x, max x = min(min x, min(x greek)), max(max x, max(x greek))
                min y, max y = min(min y, min(y greek)), max(max y, max(y greek))
            
            # Gambar Greek key di tengah sisi tile
            for side in range(4):
                side angle = side * np.pi/2
                side x = tile cx + (tile width/2 - unit size/2) * np.cos(side angle)
                side y = tile cy + (tile height/2 - unit size/2) * np.sin(side angle)
                
                side points = draw greek key unit(side x, side y, 
                                                 unit size/1.5, side angle + np.pi/4)
                
                x side = [p[0] for p in side points]
                y side = [p[1] for p in side points]
                
                ax.plot(x side, y side, color="black", linewidth=0.9, 
                       solid capstyle="round", alpha=0.8)
                
                # Update bounding box
                min x, max x = min(min x, min(x side)), max(max x, max(x side))
                min y, max y = min(min y, min(y side)), max(max y, max(y side))
    
    # Layer 2: Arabesque curves connecting the meanders
    for tx in range(n tiles x):
        for ty in range(n tiles y):
            tile cx = offset x + tx * tile width + tile width/2
            tile cy = offset y + ty * tile height + tile height/2
            
            # Arabesque di pusat tile
            arabesque size = unit size * 1.5
            
            for direction in [1, -1]:
                x arab, y arab = draw arabesque curve(tile cx, tile cy, 
                                                     arabesque size, direction)
                
                ax.plot(x arab, y arab, color="black", linewidth=0.8, 
                       solid capstyle="round", alpha=0.7)
                
                # Update bounding box
                min x, max x = min(min x, min(x arab)), max(max x, max(x arab))
                min y, max y = min(min y, min(y arab)), max(max y, max(y arab))
            
            # Arabesque kecil di antara Greek keys
            for i in range(4):
                angle = i * np.pi/2 + np.pi/4
                small x = tile cx + (tile width/3) * np.cos(angle)
                small y = tile cy + (tile height/3) * np.sin(angle)
                
                x small, y small = draw arabesque curve(small x, small y, 
                                                       unit size/2, (-1)**i)
                
                ax.plot(x small, y small, color="black", linewidth=0.6, 
                       solid capstyle="round", alpha=0.6)
                
                # Update bounding box
                min x, max x = min(min x, min(x small)), max(max x, max(x small))
                min y, max y = min(min y, min(y small)), max(max y, max(y small))
    
    # Layer 3: Connecting lines untuk seamless effect
    # Garis penghubung antara tiles
    for tx in range(n tiles x + 1):
        x conn = offset x + tx * tile width
        for ty in range(n tiles y):
            y start = offset y + ty * tile height + tile height/2
            
            # Garis vertikal penghubung
            if tx < n tiles x:  # Garis di dalam area
                ax.plot([x conn, x conn], [y start - unit size, y start + unit size],
                       color="black", linewidth=0.7, alpha=0.5)
            else:  # Garis di batas kanan (untuk menunjukkan continuity)
                ax.plot([x conn, x conn + 2], [y start - unit size, y start + unit size],
                       color="black", linewidth=0.5, alpha=0.3, linestyle=":")
    
    for ty in range(n tiles y + 1):
        y conn = offset y + ty * tile height
        for tx in range(n tiles x):
            x start = offset x + tx * tile width + tile width/2
            
            # Garis horizontal penghubung
            if ty < n tiles y:  # Garis di dalam area
                ax.plot([x start - unit size, x start + unit size], [y conn, y conn],
                       color="black", linewidth=0.7, alpha=0.5)
            else:  # Garis di batas bawah
                ax.plot([x start - unit size, x start + unit size], [y conn, y conn + 2],
                       color="black", linewidth=0.5, alpha=0.3, linestyle=":")
    
    # Layer 4: Decorative elements untuk menunjukkan seamless connections
    # Pattern continuation di luar batas
    continuation dist = 5.0
    
    # Continuation kiri
    left x = offset x - continuation dist
    for ty in range(n tiles y):
        tile cy = offset y + ty * tile height + tile height/2
        
        # Gambar sebagian pattern
        x arab, y arab = draw arabesque curve(left x, tile cy, unit size, 1)
        mask = x arab >= offset x - 2
        if mask.any():
            ax.plot(x arab[mask], y arab[mask], color="black", linewidth=0.5, 
                   alpha=0.3, linestyle="--")
    
    # Continuation kanan
    right x = offset x + n tiles x * tile width + continuation dist
    for ty in range(n tiles y):
        tile cy = offset y + ty * tile height + tile height/2
        
        x arab, y arab = draw arabesque curve(right x, tile cy, unit size, -1)
        mask = x arab <= offset x + n tiles x * tile width + 2
        if mask.any():
            ax.plot(x arab[mask], y arab[mask], color="black", linewidth=0.5, 
                   alpha=0.3, linestyle="--")
    
    # Continuation atas
    top y = offset y - continuation dist
    for tx in range(n tiles x):
        tile cx = offset x + tx * tile width + tile width/2
        
        x arab, y arab = draw arabesque curve(tile cx, top y, unit size, 1)
        mask = y arab >= offset y - 2
        if mask.any():
            ax.plot(x arab[mask], y arab[mask], color="black", linewidth=0.5, 
                   alpha=0.3, linestyle="--")
    
    # Continuation bawah
    bottom y = offset y + n tiles y * tile height + continuation dist
    for tx in range(n tiles x):
        tile cx = offset x + tx * tile width + tile width/2
        
        x arab, y arab = draw arabesque curve(tile cx, bottom y, unit size, -1)
        mask = y arab <= offset y + n tiles y * tile height + 2
        if mask.any():
            ax.plot(x arab[mask], y arab[mask], color="black", linewidth=0.5, 
                   alpha=0.3, linestyle="--")
    
    # Tunjukkan repeat unit dengan rectangle
    repeat rect = plt.Rectangle((center x - tile width, center y - tile height),
                               tile width * 2, tile height * 2,
                               fill=False, linewidth=2, edgecolor="purple", 
                               alpha=0.7, linestyle="-")
    ax.add patch(repeat rect)
    
    # Label repeat unit
    ax.text(center x, center y - tile height - 4, 
           "Seamless Repeat Unit (2×2 Tiles)", ha="center", va="top",
           fontsize=11, alpha=0.8, color="purple", weight="bold")
    
    # Tunjukkan how tiles connect dengan arrows
    # Horizontal connection
    arrow h start = center x - tile width
    arrow h end = center x + tile width
    arrow h y = center y + tile height + 6
    
    ax.annotate("", xy=(arrow h end, arrow h y), xytext=(arrow h start, arrow h y),
               arrowprops=dict(arrowstyle="<->", color="orange", lw=1.5, alpha=0.7))
    
    ax.text(center x, arrow h y + 2, "Horizontal Repeat", ha="center", va="bottom",
           fontsize=9, alpha=0.7, color="orange")
    
    # Vertical connection
    arrow v x = center x + tile width + 6
    arrow v start = center y - tile height
    arrow v end = center y + tile height
    
    ax.annotate("", xy=(arrow v x, arrow v end), xytext=(arrow v x, arrow v start),
               arrowprops=dict(arrowstyle="<->", color="orange", lw=1.5, alpha=0.7))
    
    ax.text(arrow v x + 4, center y, "Vertical Repeat", ha="left", va="center",
           fontsize=9, alpha=0.7, color="orange", rotation=90)
    
    # Framing untuk fokus pada area seamless
    display pad = 10.0
    ax.set xlim(center x - tile width - display pad, 
                center x + tile width + display pad)
    ax.set ylim(center y - tile height - display pad,
                center y + tile height + display pad)
    
    save(fig, "abstract geometric arabesque meander seamless pattern black white texture"))


if   name   == "  main  ":
    arabesque meander seamless()