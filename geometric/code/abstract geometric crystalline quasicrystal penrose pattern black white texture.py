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

PHI = (1 + np.sqrt(5)) / 2  # Rasio Emas (Golden Ratio)


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


def subdivide(triangles):
    """Subdivisi rekursif menggunakan segitiga Robinson untuk membentuk Penrose P3."""
    result = []
    for color, A, B, C in triangles:
        if color == 0:
            # Segitiga 'Fat' (Tebal)
            P = A + (B - A) / PHI
            result.append((0, C, P, B))
            result.append((1, P, C, A))
        else:
            # Segitiga 'Thin' (Tipis)
            Q = B + (A - B) / PHI
            R = B + (C - B) / PHI
            result.append((1, R, C, A))
            result.append((1, Q, R, B))
            result.append((0, R, Q, A))
    return result


def crystalline quasicrystal penrose():
    """Penrose P3 Quasicrystal Tessellation berbasis Deflasi Segitiga Robinson."""
    fig, ax = setup ax()

    # Inisialisasi 10 segitiga dasar membentuk pola Sun / Star 10-fold symmetry
    triangles = []
    center = np.array([50.0, 50.0])
    radius = 65.0

    for i in range(10):
        B = center + radius * np.array([
            np.cos((i - 0.5) * np.pi / 5),
            np.sin((i - 0.5) * np.pi / 5),
        ])
        C = center + radius * np.array([
            np.cos((i + 0.5) * np.pi / 5),
            np.sin((i + 0.5) * np.pi / 5),
        ])
        if i % 2 == 0:
            triangles.append((0, center, B, C))
        else:
            triangles.append((0, center, C, B))

    # Lakukan subdivisi rekursif (tingkat kedalaman 6 untuk kerapatan ideal)
    for   in range(6):
        triangles = subdivide(triangles)

    # Kumpulkan segmen garis unik agar tidak menggambar ulang garis yang sama
    lines = set()
    for color, A, B, C in triangles:
        # Garis luar rombus adalah sisi A-B dan B-C dari segitiga Robinson
        for p1, p2 in [(A, B), (B, C)]:
            # Bulatkan koordinat untuk kunci himpunan unik
            edge = tuple(sorted((
                (round(p1[0], 4), round(p1[1], 4)),
                (round(p2[0], 4), round(p2[1], 4)),
            )))
            lines.add(edge)

    # Plot jaringan Penrose tiling yang mulus dan presisi
    for (x1, y1), (x2, y2) in lines:
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=0.7, solid capstyle="round")

    # Atur batas tampilan simetris tepat di tengah
    pad = 42.0
    ax.set xlim(50 - pad, 50 + pad)
    ax.set ylim(50 - pad, 50 + pad)

    save(fig, "abstract geometric crystalline quasicrystal penrose pattern black white texture"))


if   name   == "  main  ":
    crystalline quasicrystal penrose()