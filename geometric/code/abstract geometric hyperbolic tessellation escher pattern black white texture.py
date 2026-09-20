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


def poincare transform(x, y, R=40.0):
    """Memetakan titik koordinat ke dalam Poincaré Disk Model secara presisi."""
    r = np.hypot(x, y)
    if r == 0:
        return 0.0, 0.0
    r transformed = R * (r / (R + r))
    theta = np.arctan2(y, x)
    return r transformed * np.cos(theta), r transformed * np.sin(theta)


def hyperbolic tessellation escher():
    """Teselasi Hiperbolik Escher tanpa garis batas lingkaran luar."""
    fig, ax = setup ax()

    cx, cy = 50.0, 50.0
    disk radius = 42.0

    # (Perintah gambar lingkaran batas luar telah dihapus dari sini)

    # Buat Kisi dasar bersarang (Nested Hexagonal / Star Lattice)
    n rings = 10
    n pts per ring = 6

    for ring in range(1, n rings + 1):
        r base = ring * 8.0
        n polygons = ring * n pts per ring

        for i in range(n polygons):
            angle = 2 * np.pi * i / n polygons
            bx = r base * np.cos(angle)
            by = r base * np.sin(angle)

            # Poligon lokal
            poly sides = 6
            poly size = 5.0 / (1.0 + 0.08 * r base)
            poly angles = np.linspace(0, 2 * np.pi, poly sides + 1) + angle

            px = bx + poly size * np.cos(poly angles)
            py = by + poly size * np.sin(poly angles)

            # Peta setiap titik ke Poincaré Disk
            tx, ty = [], []
            for x val, y val in zip(px, py):
                hx, hy = poincare transform(x val, y val, R=disk radius)
                tx.append(cx + hx)
                ty.append(cy + hy)

            # Ketebalan garis menyesuaikan kedalaman kisi
            lw = max(0.4, 1.2 - ring * 0.08)
            ax.plot(tx, ty, color="black", linewidth=lw, solid capstyle="round", zorder=2)

    # Framing simetris terpusat
    pad = disk radius + 4.0
    ax.set xlim(cx - pad, cx + pad)
    ax.set ylim(cy - pad, cy + pad)

    save(fig, "abstract geometric hyperbolic tessellation escher pattern black white texture"))


if   name   == "  main  ":
    hyperbolic tessellation escher()