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


def draw polygon(cx, cy, size, n sides, rotation=0):
    """Menggambar poligon dengan n sisi."""
    angles = np.linspace(0, 2 * np.pi, n sides + 1) + rotation
    x = cx + size * np.cos(angles)
    y = cy + size * np.sin(angles)
    return x, y


def spiral polygon fusion():
    """Fusi spiral dengan poligon yang bermetamorfosis."""
    fig, ax = setup ax()
    
    center x, center y = 50, 50
    
    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")
    
    # Parameter spiral utama
    n spiral points = 120
    spiral turns = 5.5
    max radius = 38.0
    
    # Simpan posisi spiral untuk referensi
    spiral positions = []
    
    # Layer 1: Spiral dasar dengan poligon di setiap titik
    for i in range(n spiral points):
        t = i / n spiral points
        angle = t * spiral turns * 2 * np.pi
        radius = 2.0 + max radius * (t ** 1.2)
        
        spiral x = center x + radius * np.cos(angle)
        spiral y = center y + radius * np.sin(angle)
        spiral positions.append((spiral x, spiral y, t))
        
        # Jumlah sisi poligon meningkat sepanjang spiral
        # Dari segitiga (3) ke oktagon (8) dan kembali
        n sides = int(3 + 5 * np.sin(t * np.pi * 2))
        n sides = max(3, min(8, n sides))
        
        # Ukuran poligon meningkat sepanjang spiral
        polygon size = 0.8 + 3.5 * t
        
        # Rotasi poligon mengikuti spiral
        polygon rotation = angle * 0.8 + t * np.pi
        
        # Gambar poligon
        x poly, y poly = draw polygon(spiral x, spiral y, polygon size, n sides, polygon rotation)
        
        # Ketebalan garis berdasarkan posisi spiral
        lw = 0.6 + 1.2 * (1.0 - t)
        alpha = 0.8 - 0.3 * t
        
        ax.plot(x poly, y poly, color="black", linewidth=lw, alpha=alpha)
        
        # Update bounding box
        min x, max x = min(min x, x poly.min()), max(max x, x poly.max())
        min y, max y = min(min y, y poly.min()), max(max y, y poly.max())
        
        # Tambahkan titik pusat poligon
        ax.plot(spiral x, spiral y, marker="o", markersize=0.6, 
                color="black", alpha=0.6)
    
    # Layer 2: Garis penghubung antara poligon spiral
    for i in range(len(spiral positions) - 1):
        x1, y1, t1 = spiral positions[i]
        x2, y2, t2 = spiral positions[i + 1]
        
        # Gambar garis penghubung dengan pola
        n segments = 3
        for seg in range(n segments):
            seg t1 = seg / n segments
            seg t2 = (seg + 1) / n segments
            
            # Titik di sepanjang garis dengan offset sinusoidal
            seg x1 = x1 + (x2 - x1) * seg t1
            seg y1 = y1 + (y2 - y1) * seg t1
            seg x2 = x1 + (x2 - x1) * seg t2
            seg y2 = y1 + (y2 - y1) * seg t2
            
            # Offset sinusoidal untuk efek organik
            mid t = (seg t1 + seg t2) / 2
            offset magnitude = 0.8 * (1.0 - t1)
            offset angle = (i + seg) * 0.5
            
            offset x = offset magnitude * np.sin(mid t * np.pi * 4 + offset angle)
            offset y = offset magnitude * np.cos(mid t * np.pi * 4 + offset angle)
            
            # Gambar segmen garis
            seg line x = [seg x1 + offset x * seg t1, seg x2 + offset x * seg t2]
            seg line y = [seg y1 + offset y * seg t1, seg y2 + offset y * seg t2]
            
            ax.plot(seg line x, seg line y, color="black", linewidth=0.4, alpha=0.5)
    
    # Layer 3: Poligon konsentris di pusat
    n concentric = 8
    for i in range(n concentric):
        t = i / (n concentric - 1)
        
        # Radius konsentris
        concentric radius = 12.0 * t
        
        # Jumlah sisi meningkat dari pusat ke luar
        concentric sides = 3 + int(7 * t)
        
        # Rotasi meningkat
        concentric rotation = i * 0.4
        
        # Gambar poligon konsentris
        x con, y con = draw polygon(center x, center y, concentric radius, 
                                   concentric sides, concentric rotation)
        
        lw = 0.8 + 0.8 * t
        alpha = 0.7 + 0.2 * t
        
        ax.plot(x con, y con, color="black", linewidth=lw, alpha=alpha)
        
        # Update bounding box
        min x, max x = min(min x, x con.min()), max(max x, x con.max())
        min y, max y = min(min y, y con.min()), max(max y, y con.max())
        
        # Hubungkan titik sudut ke spiral terdekat
        if i == n concentric - 1:  # Poligon terluar
            for j in range(concentric sides):
                poly x = x con[j]
                poly y = y con[j]
                
                # Cari titik spiral terdekat
                closest dist = float("inf")
                closest spiral = None
                
                for sx, sy, st in spiral positions[:20]:  # Hanya spiral dalam
                    dist = np.sqrt((poly x - sx)**2 + (poly y - sy)**2)
                    if dist < closest dist:
                        closest dist = dist
                        closest spiral = (sx, sy)
                
                if closest spiral and closest dist < 25:
                    sx, sy = closest spiral
                    
                    # Gambar garis penghubung dengan kurva
                    n curve = 15
                    t curve = np.linspace(0, 1, n curve)
                    
                    # Kurva Bezier dengan kontrol point di tengah
                    mid x = (poly x + sx) / 2 + np.random.uniform(-3, 3)
                    mid y = (poly y + sy) / 2 + np.random.uniform(-3, 3)
                    
                    curve x = (1-t curve)**2 * poly x + 2*(1-t curve)*t curve*mid x + t curve**2*sx
                    curve y = (1-t curve)**2 * poly y + 2*(1-t curve)*t curve*mid y + t curve**2*sy
                    
                    ax.plot(curve x, curve y, color="black", linewidth=0.3, alpha=0.4)
    
    # Layer 4: Poligon kecil di antara spiral
    for i in range(0, len(spiral positions) - 5, 3):
        x1, y1, t1 = spiral positions[i]
        x2, y2, t2 = spiral positions[i + 2]
        x3, y3, t3 = spiral positions[i + 4]
        
        # Posisi tengah antara tiga titik spiral
        mid x = (x1 + x2 + x3) / 3
        mid y = (y1 + y2 + y3) / 3
        
        # Ukuran berdasarkan jarak dari pusat
        center dist = np.sqrt((mid x - center x)**2 + (mid y - center y)**2)
        small size = 1.0 + 2.0 * (center dist / 40)
        
        # Poligon kecil (segitiga atau segiempat)
        small sides = 3 if i % 2 == 0 else 4
        small rotation = i * 0.2
        
        x small, y small = draw polygon(mid x, mid y, small size, small sides, small rotation)
        
        ax.plot(x small, y small, color="black", linewidth=0.5, alpha=0.6)
        
        # Update bounding box
        min x, max x = min(min x, x small.min()), max(max x, x small.max())
        min y, max y = min(min y, y small.min()), max(max y, y small.max())
        
        # Hubungkan ke titik spiral terdekat
        for sx, sy, st in [(x1, y1, t1), (x2, y2, t2), (x3, y3, t3)]:
            if np.sqrt((mid x - sx)**2 + (mid y - sy)**2) < 15:
                ax.plot([mid x, sx], [mid y, sy], color="black", 
                       linewidth=0.2, alpha=0.3)
    
    # Layer 5: Elemen spiral sekunder
    secondary center x, secondary center y = center x + 15, center y - 12
    n secondary = 40
    
    for i in range(n secondary):
        t = i / n secondary
        angle = t * 3 * 2 * np.pi
        radius = 1.5 + 8.0 * (t ** 1.5)
        
        sec x = secondary center x + radius * np.cos(angle)
        sec y = secondary center y + radius * np.sin(angle)
        
        # Poligon kecil di spiral sekunder
        sec sides = 3 + int(3 * np.sin(t * np.pi))
        sec size = 0.4 + 1.2 * t
        sec rotation = angle * 1.2
        
        x sec, y sec = draw polygon(sec x, sec y, sec size, sec sides, sec rotation)
        
        ax.plot(x sec, y sec, color="black", linewidth=0.4, alpha=0.5)
        
        # Update bounding box
        min x, max x = min(min x, x sec.min()), max(max x, x sec.max())
        min y, max y = min(min y, y sec.min()), max(max y, y sec.max())
    
    # Framing dinamis
    cx final = (min x + max x) / 2.0
    cy final = (min y + max y) / 2.0
    w = max x - min x
    h = max y - min y
    pad = max(w, h) / 2.0 + 2.0
    
    ax.set xlim(cx final - pad, cx final + pad)
    ax.set ylim(cy final - pad, cy final + pad)
    
    save(fig, "abstract geometric spiral polygon fusion pattern black white texture"))


if   name   == "  main  ":
    spiral polygon fusion()