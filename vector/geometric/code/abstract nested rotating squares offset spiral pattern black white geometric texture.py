import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

JPG DIR = Path("output/jpg")
SVG DIR = Path("output/svg")
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


def nested rotating squares offset spiral():
    """Kotak bersarang dengan posisi berpindah secara spiral dari pusat."""
    fig, ax = setup ax()
    
    n squares = 35
    center x, center y = 50, 50
    
    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")
    
    for i in range(n squares):
        # Ukuran bertambah secara progresif
        size = 1.5 + i * 2.0
        
        # Rotasi bertambah secara progresif
        angle = i * 7
        
        # Perpindahan posisi pusat secara spiral
        spiral radius = i * 0.8
        spiral angle = np.radians(i * 15)
        
        # Pusat yang berpindah
        cx = center x + spiral radius * np.cos(spiral angle)
        cy = center y + spiral radius * np.sin(spiral angle)
        
        rad = np.radians(angle)
        corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        xs = []
        ys = []
        
        for dx, dy in corners:
            rx = dx * size * np.cos(rad) - dy * size * np.sin(rad)
            ry = dx * size * np.sin(rad) + dy * size * np.cos(rad)
            xs.append(cx + rx)
            ys.append(cy + ry)
        
        xs.append(xs[0])
        ys.append(ys[0])
        
        # Melacak bounding box untuk framing
        min x, max x = min(min x, min(xs)), max(max x, max(xs))
        min y, max y = min(min y, min(ys)), max(max y, max(ys))
        
        # Ketebalan garis bervariasi
        lw = 0.8 + 1.8 * (i / n squares)
        alpha = 0.9 - 0.3 * (i / n squares)
        
        ax.plot(xs, ys, color="black", linewidth=lw, alpha=alpha)
        
        # Tambahkan titik pusat untuk setiap kotak
        ax.plot(cx, cy, marker="o", markersize=0.8, color="black", alpha=0.6)
    
    # Framing dinamis berdasarkan bounding box aktual
    cx final = (min x + max x) / 2.0
    cy final = (min y + max y) / 2.0
    w = max x - min x
    h = max y - min y
    pad = max(w, h) / 2.0 + 3.0
    
    ax.set xlim(cx final - pad, cx final + pad)
    ax.set ylim(cy final - pad, cy final + pad)
    
    save(fig, "abstract nested rotating squares offset spiral pattern black white geometric texture"))


if   name   == "  main  ":
    nested rotating squares offset spiral()