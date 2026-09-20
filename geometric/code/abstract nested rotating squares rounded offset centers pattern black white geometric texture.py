import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.transforms import Affine2D
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


def nested rotating squares rounded offset centers():
    """Kotak bersarang dengan sudut membulat dan pusat yang berpindah secara dinamis."""
    fig, ax = setup ax()
    
    n squares = 28
    main center x, main center y = 50, 50
    
    min x, max x = float("inf"), float("-inf")
    min y, max y = float("inf"), float("-inf")
    
    for i in range(n squares):
        t = i / (n squares - 1)
        
        # Ukuran bertambah
        s = 1.5 + i * 1.4
        
        # Radius sudut membesar secara progresif
        r = 0.6 * s * t
        
        # Pusat yang berpindah secara sinusoidal
        offset x = 8 * np.sin(i * 0.3) * (1 - t)
        offset y = 6 * np.cos(i * 0.25) * (1 - t)
        
        cx = main center x + offset x
        cy = main center y + offset y
        
        # Rotasi bertambah
        rotation angle = i * 6.5
        
        # Transformasi: translasi + rotasi
        tr = (Affine2D()
              .translate(cx - main center x, cy - main center y)
              .rotate deg around(main center x, main center y, rotation angle)
              + ax.transData)
        
        # Buat kotak dengan sudut membulat
        box = FancyBboxPatch(
            (main center x - s, main center y - s),
            s * 2,
            s * 2,
            boxstyle=f"round,pad=0,rounding size={r}",
            fill=False,
            edgecolor="black",
            linewidth=0.8 + 2.2 * t,
            transform=tr,
        )
        ax.add patch(box)
        
        # Hitung bounding box untuk framing
        corners = [
            (main center x - s, main center y - s),
            (main center x + s, main center y - s),
            (main center x + s, main center y + s),
            (main center x - s, main center y + s)
        ]
        
        # Terapkan transformasi ke sudut
        for corner x, corner y in corners:
            # Terapkan rotasi
            rad = np.radians(rotation angle)
            rx = (corner x - main center x) * np.cos(rad) - (corner y - main center y) * np.sin(rad)
            ry = (corner x - main center x) * np.sin(rad) + (corner y - main center y) * np.cos(rad)
            
            # Terapkan translasi
            final x = main center x + rx + offset x
            final y = main center y + ry + offset y
            
            min x, max x = min(min x, final x), max(max x, final x)
            min y, max y = min(min y, final y), max(max y, final y)
    
    # Framing dinamis berdasarkan bounding box aktual
    cx final = (min x + max x) / 2.0
    cy final = (min y + max y) / 2.0
    w = max x - min x
    h = max y - min y
    pad = max(w, h) / 2.0 + 4.0
    
    ax.set xlim(cx final - pad, cx final + pad)
    ax.set ylim(cy final - pad, cy final + pad)
    
    save(fig, "abstract nested rotating squares rounded offset centers pattern black white geometric texture"))


if   name   == "  main  ":
    nested rotating squares rounded offset centers()