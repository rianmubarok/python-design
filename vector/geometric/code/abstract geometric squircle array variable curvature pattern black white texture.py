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


def squircle array variable curvature():
    """Array squircles dengan kelengkungan variabel dari kotak hingga lingkaran."""
    fig, ax = setup ax()
    
    n cols = 8
    n rows = 8
    dx = 100 / n cols
    dy = 100 / n rows
    t vals = np.linspace(0, 2 * np.pi, 200)
    
    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")
    
    for r in range(n rows):
        for c in range(n cols):
            cx = (c + 0.5) * dx
            cy = (r + 0.5) * dy
            
            # Ukuran dasar
            r base = dx * 0.4
            
            # Eksponen squircle bervariasi dari baris ke baris
            # Baris atas: hampir kotak (p tinggi)
            # Baris bawah: hampir lingkaran (p mendekati 2)
            p = 8.0 - 6.0 * (r / (n rows - 1))
            p = max(2.1, min(8.0, p))
            
            cos t = np.cos(t vals)
            sin t = np.sin(t vals)
            
            x = cx + r base * np.sign(cos t) * (np.abs(cos t) ** (2 / p))
            y = cy + r base * np.sign(sin t) * (np.abs(sin t) ** (2 / p))
            
            # Ketebalan garis berdasarkan kelengkungan
            # Lebih tebal untuk bentuk lebih kotak
            lw = 0.8 + 1.2 * ((p - 2.0) / 6.0)
            
            # Alpha berdasarkan posisi grid
            alpha = 0.7 + 0.2 * ((c + r) % 2)
            
            ax.plot(x, y, color="black", linewidth=lw, alpha=alpha)
            
            # Melacak bounding box
            min x, max x = min(min x, x.min()), max(max x, x.max())
            min y, max y = min(min y, y.min()), max(max y, y.max())
            
            # Tambahkan titik pusat dengan ukuran berdasarkan kelengkungan
            marker size = 1.0 if p > 5 else 1.5
            ax.plot(cx, cy, marker="o", markersize=marker size, 
                    color="black", alpha=0.6)
    
    # Framing dinamis berdasarkan bounding box
    cx final = (min x + max x) / 2.0
    cy final = (min y + max y) / 2.0
    w = max x - min x
    h = max y - min y
    pad = max(w, h) / 2.0 + 3.0
    
    ax.set xlim(cx final - pad, cx final + pad)
    ax.set ylim(cy final - pad, cy final + pad)
    
    save(fig, "abstract geometric squircle array variable curvature pattern black white texture"))


if   name   == "  main  ":
    squircle array variable curvature()