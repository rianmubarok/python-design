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


def squircle array extreme curvature():
    """Array squircles dengan kelengkungan ekstrem dari sangat tajam hingga sangat bulat."""
    fig, ax = setup ax()
    
    n cols = 10
    n rows = 10
    dx = 100 / n cols
    dy = 100 / n rows
    t vals = np.linspace(0, 2 * np.pi, 300)  # Lebih banyak titik untuk presisi
    
    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")
    
    for r in range(n rows):
        for c in range(n cols):
            cx = (c + 0.5) * dx
            cy = (r + 0.5) * dy
            
            # Ukuran dengan variasi diagonal
            size factor = 0.35 + 0.1 * np.sin((c + r) * 0.3)
            r base = dx * 0.35 * size factor
            
            # Eksponen squircle bervariasi secara diagonal
            # Dari kiri atas (sangat kotak) ke kanan bawah (sangat bulat)
            diagonal progress = (c + r) / (n cols + n rows - 2)
            
            # Rentang eksponen yang ekstrem: 20 (sangat kotak) hingga 2.01 (sangat bulat)
            p = 20.0 - 18.0 * diagonal progress
            p = max(2.01, min(20.0, p))
            
            # Faktor penguatan kurva untuk efek yang lebih dramatis
            curve intensity = 1.0 + 2.0 * diagonal progress
            
            cos t = np.cos(t vals)
            sin t = np.sin(t vals)
            
            # Rumus squircle dengan modifikasi untuk efek ekstrem
            x power = (2 / p) * curve intensity
            y power = (2 / p) * curve intensity
            
            x = cx + r base * np.sign(cos t) * (np.abs(cos t) ** x power)
            y = cy + r base * np.sign(sin t) * (np.abs(sin t) ** y power)
            
            # Ketebalan garis berdasarkan kelengkungan
            # Garis lebih tebal untuk bentuk lebih kotak
            lw = 0.6 + 1.8 * (1.0 - diagonal progress)
            
            # Warna dengan variasi alpha untuk efek kedalaman
            alpha = 0.6 + 0.3 * (1.0 - abs(diagonal progress - 0.5))
            
            ax.plot(x, y, color="black", linewidth=lw, alpha=alpha)
            
            # Melacak bounding box
            min x, max x = min(min x, x.min()), max(max x, x.max())
            min y, max y = min(min y, y.min()), max(max y, y.max())
            
            # Tambahkan detail interior berdasarkan kelengkungan
            if diagonal progress < 0.3:  # Bentuk kotak
                # Tambahkan garis diagonal untuk kotak
                inner size = r base * 0.4
                ax.plot([cx - inner size, cx + inner size], 
                        [cy - inner size, cy + inner size], 
                        color="black", linewidth=0.3, alpha=0.5)
                ax.plot([cx - inner size, cx + inner size], 
                        [cy + inner size, cy - inner size], 
                        color="black", linewidth=0.3, alpha=0.5)
            elif diagonal progress > 0.7:  # Bentuk bulat
                # Tambahkan lingkaran dalam untuk bentuk bulat
                inner circle = plt.Circle((cx, cy), r base * 0.3, 
                                         fill=False, linewidth=0.4, 
                                         edgecolor="black", alpha=0.4)
                ax.add patch(inner circle)
    
    # Framing dengan padding yang sesuai
    cx final = (min x + max x) / 2.0
    cy final = (min y + max y) / 2.0
    w = max x - min x
    h = max y - min y
    pad = max(w, h) / 2.0 + 2.0
    
    ax.set xlim(cx final - pad, cx final + pad)
    ax.set ylim(cy final - pad, cy final + pad)
    
    save(fig, "squircle array extreme curvature")


if   name   == "  main  ":
    squircle array extreme curvature()