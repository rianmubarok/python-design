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
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
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


def rotate point(x, y, cx, cy, angle):
    """Menerapkan rotasi 2D pada titik (x, y) terhadap pusat (cx, cy)."""
    tx, ty = x - cx, y - cy
    rx = tx * np.cos(angle) - ty * np.sin(angle)
    ry = tx * np.sin(angle) + ty * np.cos(angle)
    return cx + rx, cy + ry


def draw islamic star(cx, cy, outer radius, inner radius, n points=8):
    """Menggambar bintang islamic dengan n titik."""
    angles = []
    radii = []
    
    for i in range(n points * 2):  # n points × 2 (outer/inner)
        angle = i * np.pi / n points
        if i % 2 == 0:
            radius = outer radius
        else:
            radius = inner radius
        angles.append(angle)
        radii.append(radius)
    
    # Tutup bentuk
    angles.append(angles[0])
    radii.append(radii[0])
    
    x = [cx + r * np.cos(a) for r, a in zip(radii, angles)]
    y = [cy + r * np.sin(a) for r, a in zip(radii, angles)]
    
    return x, y


def draw kaleidoscope triangle(cx, cy, base radius, height, rotation=0):
    """Menggambar segitiga untuk pola kaleidoskop."""
    # Titik segitiga (pusat di puncak)
    points = np.array([
        [cx, cy + height],
        [cx - base radius/2, cy],
        [cx + base radius/2, cy],
        [cx, cy + height]
    ])
    
    # Terapkan rotasi
    rotated points = []
    for x, y in points:
        rx, ry = rotate point(x, y, cx, cy, rotation)
        rotated points.append([rx, ry])
    
    return np.array(rotated points)


def arabesque kaleidoscope fusion():
    """Fusi pola arabesque islamic dengan simetri kaleidoskop."""
    fig, ax = setup ax()
    
    center x, center y = 50, 50
    n symmetry = 12  # Simetri 12-lipat
    
    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")
    
    # Layer 1: Pola islamic di pusat dengan simetri kaleidoskop
    islamic radius = 35
    for i in range(n symmetry):
        angle = i * 2 * np.pi / n symmetry
        
        # Bintang islamic di setiap posisi simetri
        star outer = 6.0
        star inner = star outer * 0.4
        
        # Posisi bintang di lingkaran
        star cx = center x + islamic radius * np.cos(angle)
        star cy = center y + islamic radius * np.sin(angle)
        
        # Gambar bintang dengan rotasi sesuai posisi
        x star, y star = draw islamic star(star cx, star cy, star outer, star inner, 6)
        ax.plot(x star, y star, color="black", linewidth=1.3, solid capstyle="round")
        
        # Hubungkan bintang dengan garis arabesque
        if i > 0:
            prev angle = (i-1) * 2 * np.pi / n symmetry
            prev cx = center x + islamic radius * np.cos(prev angle)
            prev cy = center y + islamic radius * np.sin(prev angle)
            
            # Garis lengkung menghubungkan bintang
            n curve points = 20
            t curve = np.linspace(0, 1, n curve points)
            
            # Kurva Bezier sederhana
            curve x = (1-t curve)**2 * prev cx + 2*(1-t curve)*t curve * center x + t curve**2 * star cx
            curve y = (1-t curve)**2 * prev cy + 2*(1-t curve)*t curve * center y + t curve**2 * star cy
            
            ax.plot(curve x, curve y, color="black", linewidth=0.8, alpha=0.7)
        
        # Update bounding box
        min x, max x = min(min x, min(x star)), max(max x, max(x star))
        min y, max y = min(min y, min(y star)), max(max y, max(y star))
    
    # Layer 2: Elemen kaleidoskop di antara bintang
    kaleidoscope radius = 20
    for i in range(n symmetry):
        for j in range(3):  # Tiga lapisan segitiga
            base radius = 2.5 + j * 1.5
            height = 4.0 + j * 1.2
            
            # Posisi segitiga
            triangle angle = i * 2 * np.pi / n symmetry + j * 0.1
            triangle radius = kaleidoscope radius + j * 5
            
            triangle cx = center x + triangle radius * np.cos(triangle angle)
            triangle cy = center y + triangle radius * np.sin(triangle angle)
            
            # Gambar segitiga
            triangle points = draw kaleidoscope triangle(triangle cx, triangle cy, 
                                                        base radius, height, 
                                                        triangle angle)
            
            ax.plot(triangle points[:, 0], triangle points[:, 1], 
                   color="black", linewidth=1.0 - j*0.2, alpha=0.8)
            
            # Update bounding box
            min x, max x = min(min x, triangle points[:, 0].min()), max(max x, triangle points[:, 0].max())
            min y, max y = min(min y, triangle points[:, 1].min()), max(max y, triangle points[:, 1].max())
    
    # Layer 3: Pola islamic di pusat
    center star outer = 10.0
    center star inner = center star outer * 0.35
    x center star, y center star = draw islamic star(center x, center y, 
                                                    center star outer, center star inner, 8)
    ax.plot(x center star, y center star, color="black", linewidth=1.8, solid capstyle="round")
    
    # Pola islamic sekunder di sekitar pusat
    secondary radius = 12
    for i in range(8):
        secondary angle = i * 2 * np.pi / 8
        secondary cx = center x + secondary radius * np.cos(secondary angle)
        secondary cy = center y + secondary radius * np.sin(secondary angle)
        
        # Pola islamic kecil
        small outer = 2.5
        small inner = small outer * 0.5
        x small, y small = draw islamic star(secondary cx, secondary cy, 
                                           small outer, small inner, 4)
        
        ax.plot(x small, y small, color="black", linewidth=0.9, alpha=0.7)
        
        # Update bounding box
        min x, max x = min(min x, min(x small)), max(max x, max(x small))
        min y, max y = min(min y, min(y small)), max(max y, max(y small))
    
    # Layer 4: Elemen penghubung arabesque-kaleidoskop
    connecting radius = 28
    for i in range(n symmetry):
        angle1 = i * 2 * np.pi / n symmetry
        angle2 = (i + 1) % n symmetry * 2 * np.pi / n symmetry
        
        cx1 = center x + connecting radius * np.cos(angle1)
        cy1 = center y + connecting radius * np.sin(angle1)
        cx2 = center x + connecting radius * np.cos(angle2)
        cy2 = center y + connecting radius * np.sin(angle2)
        
        # Garis penghubung dengan pola islamic
        n connect points = 25
        t connect = np.linspace(0, 1, n connect points)
        
        # Kurva dengan multiple kontrol points untuk pola arabesque
        control1 x = center x + (connecting radius + 8) * np.cos((angle1 + angle2)/2)
        control1 y = center y + (connecting radius + 8) * np.sin((angle1 + angle2)/2)
        control2 x = center x + (connecting radius - 8) * np.cos((angle1 + angle2)/2 + np.pi/6)
        control2 y = center y + (connecting radius - 8) * np.sin((angle1 + angle2)/2 + np.pi/6)
        
        # Kurva Bezier kubik
        connect x = (1-t connect)**3 * cx1 + 3*(1-t connect)**2*t connect*control1 x + \
                   3*(1-t connect)*t connect**2*control2 x + t connect**3*cx2
        connect y = (1-t connect)**3 * cy1 + 3*(1-t connect)**2*t connect*control1 y + \
                   3*(1-t connect)*t connect**2*control2 y + t connect**3*cy2
        
        ax.plot(connect x, connect y, color="black", linewidth=0.7, alpha=0.6)
    
    # Framing dinamis
    cx final = (min x + max x) / 2.0
    cy final = (min y + max y) / 2.0
    w = max x - min x
    h = max y - min y
    pad = max(w, h) / 2.0 + 5.0
    
    ax.set xlim(cx final - pad, cx final + pad)
    ax.set ylim(cy final - pad, cy final + pad)
    
    save(fig, "arabesque kaleidoscope fusion")


if   name   == "  main  ":
    arabesque kaleidoscope fusion()