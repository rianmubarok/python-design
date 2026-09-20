from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.use("Agg")

SIZE = 4000
DPI = 300
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


def rotate point(x, y, cx, cy, angle):
    """Menerapkan rotasi 2D pada titik (x, y) terhadap pusat (cx, cy)."""
    tx, ty = x - cx, y - cy
    rx = tx * np.cos(angle) - ty * np.sin(angle)
    ry = tx * np.sin(angle) + ty * np.cos(angle)
    return cx + rx, cy + ry


def kaleidoscope triangle reflection():
    """Simetri Kaleidoskop Presisi Berbasis Refleksi Cermin Sektor."""
    fig, ax = setup ax()

    cx, cy = 50.0, 50.0
    n sectors = 12  # Simetri 12-lipat (12 sektor cermin)
    sector angle = 2 * np.pi / n sectors

    # 1. Definisikan Elemen-Elemen Elegan di Dalam 1 Sektor Acuan (0 hingga sector angle)
    # Segitiga & Poligon Motif
    motif polygons = []
    for i in range(4):
        r = 12.0 + i * 8.0
        ang = sector angle * (0.2 + 0.6 * (i % 2))
        s = 2.5 + i * 0.8

        # Poligon kecil di dalam sektor acuan
        pts = np.array([
            [r * np.cos(ang), r * np.sin(ang)],
            [(r + s) * np.cos(ang + 0.05), (r + s) * np.sin(ang + 0.05)],
            [(r + s * 0.5) * np.cos(ang - 0.08), (r + s * 0.5) * np.sin(ang - 0.08)],
            [r * np.cos(ang), r * np.sin(ang)],
        ])
        motif polygons.append(pts)

    # Garis-garis lengkung aksen motif
    motif lines = []
    t = np.linspace(0.05 * sector angle, 0.95 * sector angle, 30)
    for r in [10.0, 22.0, 34.0, 42.0]:
        lx = r * np.cos(t)
        ly = r * np.sin(t)
        motif lines.append(np.column stack((lx, ly)))

    # 2. Replikasi Refleksi Cermin Kaleidoskop di Seluruh Sektor
    for k in range(n sectors):
        base angle = k * sector angle

        for pts in motif polygons:
            # Bentuk Asli Sektor (Rotasi)
            x rot, y rot = rotate point(cx + pts[:, 0], cy + pts[:, 1], cx, cy, base angle)
            ax.plot(x rot, y rot, color="black", linewidth=1.1, solid capstyle="round")

            # Bentuk Cermin Sektor (Flip Y lalu Rotasi)
            x flip, y flip = rotate point(cx + pts[:, 0], cy - pts[:, 1], cx, cy, base angle + sector angle)
            ax.plot(x flip, y flip, color="black", linewidth=1.1, solid capstyle="round")

        for line in motif lines:
            # Garis Lengkung Asli
            lx rot, ly rot = rotate point(cx + line[:, 0], cy + line[:, 1], cx, cy, base angle)
            ax.plot(lx rot, ly rot, color="black", linewidth=0.8, solid capstyle="round")

            # Garis Lengkung Cermin
            lx flip, ly flip = rotate point(cx + line[:, 0], cy - line[:, 1], cx, cy, base angle + sector angle)
            ax.plot(lx flip, ly flip, color="black", linewidth=0.8, solid capstyle="round")

    # Framing simetris penuh di tengah
    pad = 46.0
    ax.set xlim(50.0 - pad, 50.0 + pad)
    ax.set ylim(50.0 - pad, 50.0 + pad)

    save(fig, "kaleidoscope triangle reflection")


if   name   == "  main  ":
    kaleidoscope triangle reflection()