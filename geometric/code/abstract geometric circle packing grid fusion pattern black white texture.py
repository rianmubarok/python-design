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


def draw diamond grid(ax, cx, cy, grid size, cell size, rotation=0):
    """Menggambar grid berlian (diamond) dengan rotasi."""
    half cell = cell size / 2
    
    for i in range(-grid size, grid size + 1):
        for j in range(-grid size, grid size + 1):
            # Posisi pusat berlian
            diamond cx = cx + (i * cell size + j * half cell)
            diamond cy = cy + (j * cell size * 0.866)  # Faktor hexagonal
            
            # Titik berlian
            points = [
                (diamond cx, diamond cy + half cell),
                (diamond cx + half cell, diamond cy),
                (diamond cx, diamond cy - half cell),
                (diamond cx - half cell, diamond cy),
                (diamond cx, diamond cy + half cell)
            ]
            
            # Terapkan rotasi
            rotated points = []
            for px, py in points:
                dx = px - cx
                dy = py - cy
                rx = dx * np.cos(rotation) - dy * np.sin(rotation)
                ry = dx * np.sin(rotation) + dy * np.cos(rotation)
                rotated points.append((cx + rx, cy + ry))
            
            x pts = [p[0] for p in rotated points]
            y pts = [p[1] for p in rotated points]
            
            ax.plot(x pts, y pts, color="black", linewidth=0.7, alpha=0.5)
    
    return grid size * cell size * 1.5  # Return approximate radius


def circle packing grid fusion():
    """Fusi circle packing dengan grid geometri berlian."""
    fig, ax = setup ax()
    
    center x, center y = 50, 50
    
    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")
    
    # Layer 1: Grid berlian dasar
    grid radius = draw diamond grid(ax, center x, center y, 6, 5.0, rotation=0.2)
    
    # Layer 2: Circle packing di atas grid
    # Generate points dengan distribusi yang mengikuti grid berlian
    all points = []
    
    # Titik di persimpangan grid
    for i in range(-8, 9):
        for j in range(-8, 9):
            base x = center x + i * 4.5
            base y = center y + j * 4.5
            
            # Tambahkan variasi posisi mengikuti pola berlian
            if (i + j) % 2 == 0:
                offset x = np.random.uniform(-1.2, 1.2)
                offset y = np.random.uniform(-1.2, 1.2)
            else:
                offset x = np.random.uniform(-0.8, 0.8)
                offset y = np.random.uniform(-0.8, 0.8)
            
            all points.append([base x + offset x, base y + offset y])
    
    # Titik tambahan untuk kepadatan
    for   in range(80):
        angle = np.random.uniform(0, 2*np.pi)
        radius = np.random.uniform(5, grid radius * 0.8)
        x = center x + radius * np.cos(angle)
        y = center y + radius * np.sin(angle)
        all points.append([x, y])
    
    points = np.array(all points)
    
    # Filter untuk jarak minimum
    valid points = []
    min dist threshold = 4.0
    
    for pt in points:
        if not valid points:
            valid points.append(pt)
        else:
            dists = [np.linalg.norm(pt - p) for p in valid points]
            if min(dists) >= min dist threshold:
                valid points.append(pt)
    
    points = np.array(valid points)
    n points = len(points)
    
    # Tambahkan titik pembatas untuk Voronoi
    grid bounds = np.array([
        [-30, -30], [130, -30], [130, 130], [-30, 130],
        [50, -30], [130, 50], [50, 130], [-30, 50]
    ])
    all points for voronoi = np.vstack([points, grid bounds])
    vor = Voronoi(all points for voronoi)
    
    # Layer 3: Gambar garis Voronoi dengan gaya yang mengikuti grid
    for simplex in vor.ridge vertices:
        if -1 not in simplex:
            p1 = vor.vertices[simplex[0]]
            p2 = vor.vertices[simplex[1]]
            if (-20 <= p1[0] <= 120 and -20 <= p1[1] <= 120 and
                -20 <= p2[0] <= 120 and -20 <= p2[1] <= 120):
                
                # Ketebalan berdasarkan jarak dari pusat
                center dist1 = np.sqrt((p1[0] - center x)**2 + (p1[1] - center y)**2)
                center dist2 = np.sqrt((p2[0] - center x)**2 + (p2[1] - center y)**2)
                avg dist = (center dist1 + center dist2) / 2
                
                lw = 0.5 + 0.6 * (1.0 - avg dist / 50)
                alpha = 0.4 + 0.3 * (1.0 - avg dist / 50)
                
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                       color="black", linewidth=lw, alpha=alpha, 
                       linestyle=(0, (3, 2)), zorder=2)
    
    # Layer 4: Circle packing dengan variasi berdasarkan grid
    radii = np.zeros(n points)
    for i in range(n points):
        cx, cy = points[i]
        
        # Jarak ke titik tetangga terdekat
        dists = [np.linalg.norm(points[i] - points[j]) for j in range(n points) if i != j]
        r neighbor = min(dists) * 0.42
        
        # Radius berdasarkan posisi dalam grid
        grid x dist = abs(cx - center x)
        grid y dist = abs(cy - center y)
        grid factor = max(grid x dist, grid y dist) / 40
        
        # Radius lebih kecil di dekat pusat, lebih besar di tepi
        base radius = max(1.2, r neighbor * (0.9 + 0.2 * grid factor))
        radii[i] = base radius
    
    # Gambar lingkaran dengan gaya yang berbeda
    t = np.linspace(0, 2 * np.pi, 100)
    for i in range(n points):
        cx, cy = points[i]
        r = radii[i]
        
        # Tentukan gaya berdasarkan posisi
        center dist = np.sqrt((cx - center x)**2 + (cy - center y)**2)
        
        if center dist < 20:
            # Lingkaran dalam: garis solid tebal
            x circ = cx + r * np.cos(t)
            y circ = cy + r * np.sin(t)
            lw = 1.4
            alpha = 0.9
            ax.plot(x circ, y circ, color="black", linewidth=lw, 
                    solid capstyle="round", zorder=3, alpha=alpha)
            
            # Titik pusat untuk lingkaran dalam
            ax.plot(cx, cy, marker="o", markersize=1.2, 
                    color="black", zorder=4, alpha=0.8)
        elif center dist < 40:
            # Lingkaran tengah: garis putus-putus
            x circ = cx + r * np.cos(t)
            y circ = cy + r * np.sin(t)
            lw = 1.0
            alpha = 0.7
            ax.plot(x circ, y circ, color="black", linewidth=lw, 
                    linestyle=(0, (4, 2)), zorder=3, alpha=alpha)
        else:
            # Lingkaran luar: garis tipis dengan titik
            x circ = cx + r * np.cos(t)
            y circ = cy + r * np.sin(t)
            lw = 0.6
            alpha = 0.5
            ax.plot(x circ, y circ, color="black", linewidth=lw, 
                    zorder=3, alpha=alpha)
            
            # Titik di sekeliling lingkaran luar
            for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
                marker x = cx + r * np.cos(angle)
                marker y = cy + r * np.sin(angle)
                ax.plot(marker x, marker y, marker="o", markersize=0.6, 
                        color="black", zorder=4, alpha=0.6)
        
        # Update bounding box
        x circ = cx + r * np.cos(t)
        y circ = cy + r * np.sin(t)
        min x, max x = min(min x, x circ.min()), max(max x, x circ.max())
        min y, max y = min(min y, y circ.min()), max(max y, y circ.max())
    
    # Layer 5: Elemen penghubung antara circle packing dan grid
    for i in range(0, n points, 3):  # Setiap titik ketiga
        cx, cy = points[i]
        r = radii[i]
        
        # Cari titik grid terdekat (dalam bentuk grid berlian)
        grid x = round((cx - center x) / 4.5) * 4.5 + center x
        grid y = round((cy - center y) / 4.5) * 4.5 + center y
        
        # Gambar garis penghubung jika cukup dekat
        dist to grid = np.sqrt((cx - grid x)**2 + (cy - grid y)**2)
        if dist to grid < 15:
            # Garis penghubung dengan pola
            n connect = 10
            t connect = np.linspace(0, 1, n connect)
            
            # Kurva Bezier kuadratik
            control x = (cx + grid x) / 2 + np.random.uniform(-2, 2)
            control y = (cy + grid y) / 2 + np.random.uniform(-2, 2)
            
            connect x = (1-t connect)**2 * cx + 2*(1-t connect)*t connect*control x + t connect**2*grid x
            connect y = (1-t connect)**2 * cy + 2*(1-t connect)*t connect*control y + t connect**2*grid y
            
            ax.plot(connect x, connect y, color="black", linewidth=0.4, alpha=0.4)
    
    # Framing dinamis
    cx final = (min x + max x) / 2.0
    cy final = (min y + max y) / 2.0
    w = max x - min x
    h = max y - min y
    pad = max(w, h) / 2.0 + 3.0
    
    ax.set xlim(cx final - pad, cx final + pad)
    ax.set ylim(cy final - pad, cy final + pad)
    
    save(fig, "circle packing grid fusion")


if   name   == "  main  ":
    circle packing grid fusion()