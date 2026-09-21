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


def draw triangle(cx, cy, size, rotation=0):
    """Menggambar segitiga sama sisi."""
    angles = np.array([0, 2*np.pi/3, 4*np.pi/3]) + rotation
    x = cx + size * np.cos(angles)
    y = cy + size * np.sin(angles)
    # Tutup segitiga
    x = np.append(x, x[0])
    y = np.append(y, y[0])
    return x, y


def draw hexagon(cx, cy, size, rotation=0):
    """Menggambar heksagon beraturan."""
    angles = np.linspace(0, 2*np.pi, 7) + rotation  # 6 sisi + penutup
    x = cx + size * np.cos(angles)
    y = cy + size * np.sin(angles)
    return x, y


def triangle hexagon semiregular seamless():
    """Teselasi semiregular segitiga-heksagon (3.6.3.6) yang seamless."""
    fig, ax = setup ax()
    
    # Parameter tiling
    triangle size = 4.0  # Radius segitiga
    hexagon size = triangle size * 2 / np.sqrt(3)  # Radius heksagon untuk pas
    
    # Jarak unit untuk tiling
    unit x = triangle size * 3
    unit y = triangle size * np.sqrt(3)
    
    # Jumlah unit untuk coverage
    n units x = 6
    n units y = 6
    
    # Pusat pattern
    center x, center y = 50, 50
    
    # Hitung offset untuk memusatkan
    offset x = center x - (n units x * unit x) / 2
    offset y = center y - (n units y * unit y) / 2
    
    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")
    
    # Gambar pattern untuk setiap unit
    for ux in range(n units x + 1):  # +1 untuk coverage seamless
        for uy in range(n units y + 1):
            base x = offset x + ux * unit x
            base y = offset y + uy * unit y
            
            # Unit pattern dasar: segitiga dan heksagon
            # Pattern 3.6.3.6: segitiga-heksagon-segitiga-heksagon
            
            # Heksagon di pusat unit
            hex cx = base x + unit x / 2
            hex cy = base y + unit y / 2
            
            x hex, y hex = draw hexagon(hex cx, hex cy, hexagon size, rotation=np.pi/6)
            ax.plot(x hex, y hex, color="black", linewidth=1.2, solid capstyle="round")
            
            # Update bounding box
            min x, max x = min(min x, x hex.min()), max(max x, x hex.max())
            min y, max y = min(min y, y hex.min()), max(max y, y hex.max())
            
            # Segitiga di sekitar heksagon
            for i in range(6):
                angle = i * np.pi / 3 + np.pi/6
                tri cx = hex cx + hexagon size * 1.5 * np.cos(angle)
                tri cy = hex cy + hexagon size * 1.5 * np.sin(angle)
                
                x tri, y tri = draw triangle(tri cx, tri cy, triangle size, rotation=angle)
                ax.plot(x tri, y tri, color="black", linewidth=1.0, solid capstyle="round")
                
                # Update bounding box
                min x, max x = min(min x, x tri.min()), max(max x, x tri.max())
                min y, max y = min(min y, y tri.min()), max(max y, y tri.max())
            
            # Heksagon kecil di sudut
            for i in range(6):
                angle = i * np.pi / 3
                small hex cx = hex cx + hexagon size * np.sqrt(3) * np.cos(angle)
                small hex cy = hex cy + hexagon size * np.sqrt(3) * np.sin(angle)
                
                x small hex, y small hex = draw hexagon(small hex cx, small hex cy, 
                                                       hexagon size/2, rotation=angle)
                ax.plot(x small hex, y small hex, color="black", linewidth=0.8, 
                       solid capstyle="round", alpha=0.8)
                
                # Update bounding box
                min x, max x = min(min x, x small hex.min()), max(max x, x small hex.max())
                min y, max y = min(min y, y small hex.min()), max(max y, y small hex.max())
    
    # Gambar continuation lines untuk menunjukkan seamless nature
    # Garis batas tiling
    for ux in range(n units x + 1):
        x line = offset x + ux * unit x
        ax.axvline(x=x line, color="gray", linewidth=0.4, alpha=0.3, linestyle="--")
    
    for uy in range(n units y + 1):
        y line = offset y + uy * unit y
        ax.axhline(y=y line, color="gray", linewidth=0.4, alpha=0.3, linestyle="--")
    
    # Tunjukkan unit tile dasar
    tile width = unit x * 2  # 2 unit untuk pattern lengkap
    tile height = unit y * 2
    
    # Rectangle untuk menunjukkan repeat unit
    tile rect = plt.Rectangle((center x - tile width/2, center y - tile height/2),
                             tile width, tile height,
                             fill=False, linewidth=1.5, edgecolor="blue", 
                             alpha=0.6, linestyle="-")
    ax.add patch(tile rect)
    
    # Label repeat unit
    ax.text(center x, center y - tile height/2 - 3, 
           "Seamless Repeat Unit", ha="center", va="top",
           fontsize=10, alpha=0.8, color="blue", weight="bold")
    
    # Gambar pattern continuation di luar batas untuk menunjukkan seamless
    # Continuation kiri
    cont x = offset x - unit x
    for uy in range(n units y + 1):
        base y = offset y + uy * unit y
        
        # Gambar sebagian pattern untuk menunjukkan continuity
        hex cx = cont x + unit x / 2
        hex cy = base y + unit y / 2
        
        x hex, y hex = draw hexagon(hex cx, hex cy, hexagon size, rotation=np.pi/6)
        # Filter hanya bagian yang terlihat
        mask = x hex >= offset x - 5
        if mask.any():
            ax.plot(x hex[mask], y hex[mask], color="black", linewidth=0.7, 
                   alpha=0.5, linestyle=":")
    
    # Continuation kanan
    cont x = offset x + (n units x + 1) * unit x
    for uy in range(n units y + 1):
        base y = offset y + uy * unit y
        
        hex cx = cont x + unit x / 2
        hex cy = base y + unit y / 2
        
        x hex, y hex = draw hexagon(hex cx, hex cy, hexagon size, rotation=np.pi/6)
        mask = x hex <= offset x + n units x * unit x + 5
        if mask.any():
            ax.plot(x hex[mask], y hex[mask], color="black", linewidth=0.7, 
                   alpha=0.5, linestyle=":")
    
    # Continuation atas
    cont y = offset y - unit y
    for ux in range(n units x + 1):
        base x = offset x + ux * unit x
        
        hex cx = base x + unit x / 2
        hex cy = cont y + unit y / 2
        
        x hex, y hex = draw hexagon(hex cx, hex cy, hexagon size, rotation=np.pi/6)
        mask = y hex >= offset y - 5
        if mask.any():
            ax.plot(x hex[mask], y hex[mask], color="black", linewidth=0.7, 
                   alpha=0.5, linestyle=":")
    
    # Continuation bawah
    cont y = offset y + (n units y + 1) * unit y
    for ux in range(n units x + 1):
        base x = offset x + ux * unit x
        
        hex cx = base x + unit x / 2
        hex cy = cont y + unit y / 2
        
        x hex, y hex = draw hexagon(hex cx, hex cy, hexagon size, rotation=np.pi/6)
        mask = y hex <= offset y + n units y * unit y + 5
        if mask.any():
            ax.plot(x hex[mask], y hex[mask], color="black", linewidth=0.7, 
                   alpha=0.5, linestyle=":")
    
    # Diagram showing how tiles connect
    # Draw arrows between tiles
    arrow start x = center x - tile width/4
    arrow end x = center x + tile width/4
    arrow y = center y + tile height/2 + 8
    
    ax.annotate("", xy=(arrow end x, arrow y), xytext=(arrow start x, arrow y),
               arrowprops=dict(arrowstyle="<->", color="green", lw=1.5, alpha=0.7))
    
    ax.text(center x, arrow y + 2, "Tile Connection", ha="center", va="bottom",
           fontsize=9, alpha=0.7, color="green")
    
    # Framing untuk fokus pada area seamless
    display pad = 8.0
    ax.set xlim(center x - tile width/2 - display pad, 
                center x + tile width/2 + display pad)
    ax.set ylim(center y - tile height/2 - display pad,
                center y + tile height/2 + display pad)
    
    save(fig, "abstract geometric triangle hexagon semiregular seamless pattern black white texture"))


if   name   == "  main  ":
    triangle hexagon semiregular seamless()